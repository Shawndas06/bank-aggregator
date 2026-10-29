"""
API роутер для целей накопления
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.dependencies import get_current_user
from src.models.user import User
from src.models.savings_goal import SavingsGoal
from src.services.savings_service import SavingsService
from src.schemas.savings import (
    SavingsGoalCreate,
    SavingsGoalUpdate,
    SavingsGoalResponse,
    ContributionRuleCreate,
    ContributionRuleResponse
)
from typing import List


router = APIRouter(prefix="/api/savings", tags=["Savings Goals"])


@router.post("/goals", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_savings_goal(
    goal_data: SavingsGoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создать цель накопления
    
    Примеры целей:
    - Отпуск в Турции: 150,000₽
    - Новый iPhone: 80,000₽
    - Ремонт квартиры: 500,000₽
    """
    goal, error = SavingsService.create_goal(
        db,
        current_user.id,
        goal_data.name,
        goal_data.target_amount,
        goal_data.description,
        goal_data.target_account_id,
        goal_data.target_date,
        goal_data.image_url
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Добавляем правила пополнения если есть
    for rule_data in goal_data.contribution_rules:
        SavingsService.add_contribution_rule(
            db,
            goal.id,
            current_user.id,
            rule_data.source_account_id,
            rule_data.rule_type,
            rule_data.fixed_amount,
            rule_data.percentage
        )
    
    db.refresh(goal)
    progress = SavingsService.calculate_progress(goal)
    
    return {
        "success": True,
        "data": {
            "message": "Цель успешно создана!",
            "goal": {
                "id": goal.id,
                "name": goal.name,
                "description": goal.description,
                "targetAmount": goal.target_amount,
                "currentAmount": goal.current_amount,
                "progressPercentage": progress["progress_percentage"],
                "status": goal.status.value,
                "targetDate": goal.target_date.isoformat() if goal.target_date else None,
                "imageUrl": goal.image_url,
                "estimatedCompletion": progress["estimated_completion_date"].isoformat() if progress["estimated_completion_date"] else None,
                "createdAt": goal.created_at.isoformat()
            }
        }
    }


@router.get("/goals", response_model=dict)
async def get_savings_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить все цели пользователя"""
    goals = SavingsService.get_user_goals(db, current_user.id)
    
    return {
        "success": True,
        "data": [
            {
                "id": g.id,
                "name": g.name,
                "description": g.description,
                "targetAmount": g.target_amount,
                "currentAmount": g.current_amount,
                "progressPercentage": SavingsService.calculate_progress(g)["progress_percentage"],
                "status": g.status.value,
                "targetDate": g.target_date.isoformat() if g.target_date else None,
                "imageUrl": g.image_url,
                "createdAt": g.created_at.isoformat(),
                "estimatedCompletion": SavingsService.calculate_progress(g)["estimated_completion_date"].isoformat() if SavingsService.calculate_progress(g)["estimated_completion_date"] else None
            }
            for g in goals
        ]
    }


@router.post("/goals/{goal_id}/contribute", response_model=dict)
async def contribute_to_goal(
    goal_id: int,
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Внести средства в цель"""
    
    success, error = SavingsService.contribute_to_goal(
        db,
        goal_id,
        current_user.id,
        amount
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    # Получаем обновленную цель
    goal = db.query(SavingsGoal).filter(SavingsGoal.id == goal_id).first()
    progress = SavingsService.calculate_progress(goal)
    
    message = "Средства внесены!"
    if goal.status == "completed":
        message = "🎉 Поздравляем! Цель достигнута!"
    
    return {
        "success": True,
        "data": {
            "message": message,
            "goal": {
                "id": goal.id,
                "currentAmount": goal.current_amount,
                "progressPercentage": progress["progress_percentage"],
                "status": goal.status.value,
                "isCompleted": goal.status == "completed"
            }
        }
    }


@router.delete("/goals/{goal_id}", response_model=dict)
async def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Удалить цель"""
    
    goal = db.query(SavingsGoal).filter(
        SavingsGoal.id == goal_id,
        SavingsGoal.user_id == current_user.id
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Цель не найдена"
        )
    
    db.delete(goal)
    db.commit()
    
    return {
        "success": True,
        "data": {
            "message": "Цель удалена"
        }
    }


@router.post("/goals/{goal_id}/rules", response_model=dict)
async def add_rule_to_goal(
    goal_id: int,
    rule_data: ContributionRuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Добавить правило пополнения к цели"""
    
    rule, error = SavingsService.add_contribution_rule(
        db,
        goal_id,
        current_user.id,
        rule_data.source_account_id,
        rule_data.rule_type,
        rule_data.fixed_amount,
        rule_data.percentage
    )
    
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return {
        "success": True,
        "data": {
            "message": "Правило добавлено!",
            "rule": {
                "id": rule.id,
                "ruleType": rule.rule_type.value,
                "sourceAccountId": rule.source_account_id,
                "fixedAmount": rule.fixed_amount,
                "percentage": rule.percentage
            }
        }
    }

