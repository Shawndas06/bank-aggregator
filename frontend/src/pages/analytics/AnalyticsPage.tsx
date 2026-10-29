import {
  useGetAdvancedInsights,
  useGetAnalyticsOverview,
  useGetCategoriesBreakdown,
} from '@entities/analytics'
import { useGetMe } from '@entities/user'
import { formatCurrency } from '@shared/lib/utils'
import { Button, Card, CardContent, Progress } from '@shared/ui'
import { CategoryBadge } from '@shared/ui/category-icon'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { MobileHeader } from '@widgets/header'
import { motion } from 'framer-motion'
import {
  Activity,
  BarChart3,
  Calendar,
  Crown,
  Lightbulb,
  Lock,
  PieChart,
  Target,
  TrendingDown,
  TrendingUp,
  TrendingUpIcon,
  Wallet,
} from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export function AnalyticsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState<'week' | 'month' | 'year'>('month')
  const { data: overview, isLoading } = useGetAnalyticsOverview()
  const { data: categories } = useGetCategoriesBreakdown()
  const { data: insightsData } = useGetAdvancedInsights()
  const { data: user } = useGetMe()
  const navigate = useNavigate()
  
  const isPremium = user?.accountType === 'premium'
  const insights = insightsData

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 pb-20">
        <MobileHeader />
        <main className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <div className="mx-auto mb-4 h-12 w-12 animate-spin rounded-full border-4 border-purple-600 border-t-transparent" />
              <p className="text-lg font-semibold text-gray-900">Загрузка аналитики...</p>
              <p className="mt-2 text-sm text-gray-600">Анализируем ваши транзакции</p>
            </div>
          </div>
        </main>
        <BottomNavigation />
      </div>
    )
  }

  if (!overview) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 pb-20">
        <MobileHeader />
        <main className="container mx-auto px-4 py-6">
          <Card>
            <CardContent className="p-8 text-center">
              <PieChart className="mx-auto mb-4 h-16 w-16 text-gray-400" />
              <h3 className="mb-2 text-lg font-semibold text-gray-900">
                Нет данных для аналитики
              </h3>
              <p className="text-sm text-gray-600">
                Подключите банк и совершите транзакции
              </p>
            </CardContent>
          </Card>
        </main>
        <BottomNavigation />
      </div>
    )
  }

  const data = overview
  const currentMonth = data.currentMonth || {}
  const topCategories = data.topCategories || []
  const totalBalance = data.totalBalance || 0
  const expenses = currentMonth.expenses || 0
  const income = currentMonth.income || 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-blue-50 to-indigo-100 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-3 sm:px-4 py-4 sm:py-6 space-y-4 sm:space-y-6 max-w-4xl">
        {/* Заголовок */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2 className="mb-1 sm:mb-2 text-xl sm:text-2xl font-bold text-gray-900">Аналитика</h2>
          <p className="text-sm sm:text-base text-gray-600">Детальный анализ ваших финансов</p>
        </motion.div>

        {/* Выбор периода */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="flex justify-center gap-1.5 sm:gap-2 rounded-xl bg-white/80 backdrop-blur-sm p-1.5 sm:p-2 shadow-lg border border-white/20">
            <Button
              variant={selectedPeriod === 'week' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setSelectedPeriod('week')}
              className="flex-1 text-xs sm:text-sm py-2 sm:py-2.5"
            >
              Неделя
            </Button>
            <Button
              variant={selectedPeriod === 'month' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setSelectedPeriod('month')}
              className="flex-1 text-xs sm:text-sm py-2 sm:py-2.5"
            >
              Месяц
            </Button>
            <Button
              variant={selectedPeriod === 'year' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setSelectedPeriod('year')}
              className="flex-1 text-xs sm:text-sm py-2 sm:py-2.5"
            >
              Год
            </Button>
          </div>
        </motion.div>

        {/* Карточки баланса */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-3 gap-2 sm:gap-4"
        >
          {/* Баланс */}
          <Card className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
            <CardContent className="p-2.5 sm:p-4">
              <div className="mb-1 sm:mb-2 flex items-center gap-1 sm:gap-2 text-purple-600">
                <Wallet className="h-3 w-3 sm:h-4 sm:w-4" />
                <p className="text-[10px] sm:text-xs font-medium">Баланс</p>
              </div>
              <p className="text-sm sm:text-xl font-bold text-gray-900 truncate">
                {formatCurrency(totalBalance, 'RUB').split('.')[0]}
              </p>
            </CardContent>
          </Card>

          {/* Расходы */}
          <Card className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
            <CardContent className="p-2.5 sm:p-4">
              <div className="mb-1 sm:mb-2 flex items-center gap-1 sm:gap-2 text-red-600">
                <TrendingDown className="h-3 w-3 sm:h-4 sm:w-4" />
                <p className="text-[10px] sm:text-xs font-medium">Расходы</p>
              </div>
              <p className="text-sm sm:text-xl font-bold text-gray-900 truncate">
                {formatCurrency(expenses, 'RUB').split('.')[0]}
              </p>
            </CardContent>
          </Card>

          {/* Доходы */}
          <Card className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
            <CardContent className="p-2.5 sm:p-4">
              <div className="mb-1 sm:mb-2 flex items-center gap-1 sm:gap-2 text-green-600">
                <TrendingUp className="h-3 w-3 sm:h-4 sm:w-4" />
                <p className="text-[10px] sm:text-xs font-medium">Доходы</p>
              </div>
              <p className="text-sm sm:text-xl font-bold text-gray-900 truncate">
                {formatCurrency(income, 'RUB').split('.')[0]}
              </p>
            </CardContent>
          </Card>
        </motion.div>

        {/* Топ категории */}
        {topCategories && topCategories.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h3 className="mb-3 sm:mb-4 text-base sm:text-lg font-semibold text-gray-900">Топ категории расходов</h3>
            <div className="space-y-3">
              {topCategories.map((cat) => (
                <Card key={cat.category} className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-3">
                        <CategoryBadge category={cat.category} categoryName={cat.categoryName} />
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900">
                          {formatCurrency(cat.amount, 'RUB')}
                        </p>
                        <p className="text-sm text-gray-600">{cat.percentage}%</p>
                      </div>
                    </div>
                    <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-purple-500 rounded-full"
                        style={{ width: `${cat.percentage}%` }}
                      />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </motion.div>
        )}

        {/* Все категории */}
        {categories && categories.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Все категории</h3>
            <div className="space-y-3">
              {categories.map((cat) => (
                <Card key={cat.category} className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <CategoryBadge category={cat.category} categoryName={cat.categoryName} />
                        <p className="text-sm text-gray-600">
                          {cat.count} {cat.count === 1 ? 'транз.' : 'транз.'}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className="font-semibold text-gray-900">
                          {formatCurrency(cat.amount, 'RUB')}
                        </p>
                        <p className="text-sm text-gray-600">{cat.percentage}%</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </motion.div>
        )}

            {/* Premium Analytics Block */}
        {!isPremium && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="border-2 border-purple-200/80 bg-gradient-to-br from-purple-100/90 via-blue-50/90 to-indigo-100/90 backdrop-blur-sm shadow-lg">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 p-3">
                    <Crown className="h-6 w-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <h3 className="mb-2 flex items-center gap-2 text-lg font-bold text-gray-900">
                      <Lock className="h-5 w-5 text-purple-600" />
                      Премиум аналитика
                    </h3>
                    <p className="mb-4 text-sm text-gray-700">
                      Получите доступ к профессиональным инструментам анализа:
                    </p>
                    <ul className="mb-4 space-y-2 text-sm text-gray-700">
                      <li className="flex items-center gap-2">
                        <BarChart3 className="h-4 w-4 text-purple-600" />
                        <span>Интерактивные графики расходов и доходов</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-purple-600" />
                        <span>Прогноз бюджета на следующий месяц</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <TrendingUpIcon className="h-4 w-4 text-purple-600" />
                        <span>Анализ трендов и сезонных паттернов</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <Activity className="h-4 w-4 text-purple-600" />
                        <span>Детальная разбивка по дням и часам</span>
                      </li>
                      <li className="flex items-center gap-2">
                        <Target className="h-4 w-4 text-purple-600" />
                        <span>Цели накопления с прогресс-баром</span>
                      </li>
                    </ul>
                    <Button
                      onClick={() => navigate('/premium')}
                      className="w-full bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:from-purple-700 hover:to-blue-700"
                    >
                      <Crown className="mr-2 h-4 w-4" />
                      Получить Premium за 299 ₽/месяц
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Premium-only: Advanced Charts */}
        {isPremium && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <h3 className="mb-4 flex items-center gap-2 text-lg font-semibold text-gray-900">
              <BarChart3 className="h-5 w-5 text-purple-600" />
              Расширенная аналитика
              <span className="ml-2 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 px-2 py-0.5 text-xs font-bold text-white">
                PREMIUM
              </span>
            </h3>
            
            {/* График расходов по дням */}
            <Card className="mb-4 bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
              <CardContent className="p-6">
                <h4 className="mb-4 font-semibold text-gray-900">График расходов за месяц</h4>
                <div className="h-48 rounded-lg bg-gradient-to-br from-purple-50 to-blue-50 p-4">
                  <div className="flex h-full items-end justify-between gap-2">
                    {[65, 85, 45, 70, 90, 55, 75, 60, 80, 70, 65, 90, 100, 75, 60, 85, 70, 55, 65, 80, 75, 60, 70, 85, 90, 75, 65, 80, 70, 60].map((height, index) => (
                      <div
                        key={index}
                        className="flex-1 rounded-t-lg bg-gradient-to-t from-purple-500 to-purple-400 transition-all hover:from-purple-600 hover:to-purple-500"
                        style={{ height: `${height}%` }}
                        title={`День ${index + 1}: ${(height * 200).toFixed(0)} ₽`}
                      />
                    ))}
                  </div>
                </div>
                <div className="mt-3 flex items-center justify-between text-xs text-gray-600">
                  <span>1</span>
                  <span>15</span>
                  <span>30</span>
                </div>
              </CardContent>
            </Card>

            {/* Прогноз на следующий месяц */}
            <Card className="mb-4 border-2 border-blue-200/80 bg-white/70 backdrop-blur-sm shadow-lg">
              <CardContent className="p-6">
                <h4 className="mb-3 flex items-center gap-2 font-semibold text-gray-900">
                  <TrendingUp className="h-5 w-5 text-blue-600" />
                  Прогноз на следующий месяц
                </h4>
                <div className="space-y-3">
                  <div>
                    <div className="mb-1 flex items-center justify-between text-sm">
                      <span className="text-gray-700">Ожидаемые расходы</span>
                      <span className="font-semibold text-red-600">
                        {formatCurrency((expenses * 1.05), 'RUB')}
                      </span>
                    </div>
                    <Progress value={75} className="h-2" indicatorColor="bg-red-500" />
                  </div>
                  <div>
                    <div className="mb-1 flex items-center justify-between text-sm">
                      <span className="text-gray-700">Ожидаемые доходы</span>
                      <span className="font-semibold text-green-600">
                        {formatCurrency((income * 1.02), 'RUB')}
                      </span>
                    </div>
                    <Progress value={85} className="h-2" indicatorColor="bg-green-500" />
                  </div>
                  <div className="mt-4 rounded-lg bg-blue-50 p-3">
                    <p className="text-sm font-medium text-blue-900">
                      💡 Прогнозируемый остаток: {formatCurrency((income * 1.02 - expenses * 1.05), 'RUB')}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Распределение по часам */}
            <Card className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
              <CardContent className="p-6">
                <h4 className="mb-4 font-semibold text-white">Активность по времени суток</h4>
                <div className="space-y-2">
                  {[
                    { time: '🌅 Утро (6-12)', percent: 25, color: 'bg-yellow-500' },
                    { time: '☀️ День (12-18)', percent: 45, color: 'bg-orange-500' },
                    { time: '🌆 Вечер (18-22)', percent: 65, color: 'bg-purple-500' },
                    { time: '🌙 Ночь (22-6)', percent: 10, color: 'bg-blue-600' },
                  ].map((item) => (
                    <div key={item.time}>
                      <div className="mb-1 flex items-center justify-between text-sm">
                        <span>{item.time}</span>
                        <span className="font-medium">{item.percent}%</span>
                      </div>
                      <Progress value={item.percent} className="h-2" indicatorColor={item.color} />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Расширенные выводы и советы */}
        {insights && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: isPremium ? 0.6 : 0.5 }}
            className="space-y-4"
          >
            {/* Метрики */}
            {insights.metrics && (
              <Card className="bg-gradient-to-br from-blue-100/80 to-purple-100/80 backdrop-blur-sm border-white/30 shadow-lg">
                <CardContent className="p-4">
                  <h3 className="mb-3 flex items-center gap-2 text-lg font-semibold text-gray-900">
                    <Activity className="h-5 w-5 text-blue-600" />
                    Ключевые метрики
                  </h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="rounded-lg bg-white/90 backdrop-blur-sm p-3 shadow-md">
                      <p className="text-xs text-gray-500">Норма сбережений</p>
                      <p className={`text-xl font-bold ${insights.metrics.savingsRate >= 20 ? 'text-green-600' : insights.metrics.savingsRate < 0 ? 'text-red-600' : 'text-orange-600'}`}>
                        {insights.metrics.savingsRate.toFixed(1)}%
                      </p>
                    </div>
                    <div className="rounded-lg bg-white/90 backdrop-blur-sm p-3 shadow-md">
                      <p className="text-xs text-gray-500">Средний расход/день</p>
                      <p className="text-xl font-bold text-gray-900">
                        {formatCurrency(insights.metrics.avgDailyExpense, 'RUB')}
                      </p>
                    </div>
                    <div className="rounded-lg bg-white/90 backdrop-blur-sm p-3 shadow-md">
                      <p className="text-xs text-gray-500">Средний доход/день</p>
                      <p className="text-xl font-bold text-green-600">
                        {formatCurrency(insights.metrics.avgDailyIncome, 'RUB')}
                      </p>
                    </div>
                    <div className="rounded-lg bg-white/90 backdrop-blur-sm p-3 shadow-md">
                      <p className="text-xs text-gray-500">Соотношение расход/доход</p>
                      <p className="text-xl font-bold text-gray-900">
                        {insights.metrics.expenseToIncomeRatio.toFixed(1)}%
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Предупреждения */}
            {insights.warnings && insights.warnings.length > 0 && (
              <div className="space-y-2">
                {insights.warnings.map((warning, index: number) => (
                  <Card key={index} className={`border-2 backdrop-blur-sm shadow-lg ${warning.type === 'critical' ? 'border-red-300/80 bg-red-50/90' : 'border-orange-300/80 bg-orange-50/90'}`}>
                    <CardContent className="p-4">
                      <div className="flex items-start gap-3">
                        <div className={`rounded-full p-2 ${warning.type === 'critical' ? 'bg-red-200' : 'bg-orange-200'}`}>
                          <Target className={`h-5 w-5 ${warning.type === 'critical' ? 'text-red-600' : 'text-orange-600'}`} />
                        </div>
                        <div className="flex-1">
                          <h4 className="mb-1 font-semibold text-gray-900">{warning.title}</h4>
                          <p className="mb-2 text-sm text-gray-700">{warning.message}</p>
                          {warning.action && (
                            <Button variant="outline" size="sm" className="text-xs">
                              {warning.action}
                            </Button>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Положительные выводы */}
            {insights.insights && insights.insights.length > 0 && (
              <div className="space-y-2">
                {insights.insights.map((insight, index: number) => (
                  <Card key={index} className="border-2 border-green-300/80 bg-green-50/90 backdrop-blur-sm shadow-lg">
                    <CardContent className="p-4">
                      <div className="flex items-start gap-3">
                        <div className="rounded-full bg-green-200 p-2">
                          <span className="text-xl">{insight.icon || '✅'}</span>
                        </div>
                        <div className="flex-1">
                          <h4 className="mb-1 font-semibold text-gray-900">{insight.title}</h4>
                          <p className="text-sm text-gray-700">{insight.message}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}

            {/* Рекомендации */}
            {insights.recommendations && insights.recommendations.length > 0 && (
              <Card className="bg-gradient-to-r from-purple-100/80 to-blue-100/80 backdrop-blur-sm border-white/30 shadow-lg">
                <CardContent className="p-4">
                  <h3 className="mb-3 flex items-center gap-2 text-lg font-semibold text-gray-900">
                    <Lightbulb className="h-5 w-5 text-purple-600" />
                    Рекомендации
                  </h3>
                  <div className="space-y-2">
                    {insights.recommendations.map((rec, index: number) => (
                      <div key={index} className="rounded-lg bg-white/90 backdrop-blur-sm p-3 shadow-md">
                        <h4 className="mb-1 font-medium text-gray-900">{rec.title}</h4>
                        <p className="text-sm text-gray-700">{rec.message}</p>
                        {rec.action && (
                          <Button variant="ghost" size="sm" className="mt-2 text-xs">
                            {rec.action} →
                          </Button>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Цели */}
            {insights.goals && insights.goals.length > 0 && (
              <Card className="bg-white/70 backdrop-blur-sm border-white/30 shadow-lg">
                <CardContent className="p-4">
                  <h3 className="mb-3 flex items-center gap-2 text-lg font-semibold text-white">
                    <Target className="h-5 w-5 text-purple-400" />
                    Цели
                  </h3>
                  <div className="space-y-3">
                    {insights.goals.map((goal, index: number) => (
                      <div key={index}>
                        <div className="mb-2 flex items-center justify-between">
                          <span className="text-sm font-medium text-white">{goal.title}</span>
                          {goal.status === 'completed' && (
                            <span className="rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-700">
                              ✓ Выполнено
                            </span>
                          )}
                        </div>
                        {goal.progress !== undefined && (
                          <Progress value={goal.progress} className="h-2" />
                        )}
                        <p className="mt-1 text-xs text-gray-400">{goal.message}</p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </motion.div>
        )}
      </main>

      <BottomNavigation />
    </div>
  )
}

