import { useState } from 'react'
import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { Card, CardContent, Button } from '@shared/ui'
import { useGetAnalyticsOverview, useGetCategoriesBreakdown } from '@entities/analytics'
import { formatCurrency } from '@shared/lib/utils'
import { 
  TrendingUp, 
  TrendingDown, 
  Wallet,
  ArrowUpCircle,
  ArrowDownCircle,
  PieChart,
  Lightbulb,
  Target
} from 'lucide-react'
import { CategoryBadge } from '@shared/ui/category-icon'

export function AnalyticsPage() {
  const [selectedPeriod, setSelectedPeriod] = useState<'week' | 'month' | 'year'>('month')
  const { data: overview, isLoading } = useGetAnalyticsOverview()
  const { data: categories } = useGetCategoriesBreakdown()

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

  const data = overview.data || overview
  const currentMonth = data.currentMonth || {}
  const topCategories = data.topCategories || []
  const totalBalance = data.totalBalance || 0
  const expenses = currentMonth.expenses || 0
  const income = currentMonth.income || 0
  const expenseChange = currentMonth.expenseChange || 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6 space-y-6">
        {/* Заголовок */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h2 className="mb-2 text-2xl font-bold text-gray-900">Аналитика</h2>
          <p className="text-gray-600">Детальный анализ ваших финансов</p>
        </motion.div>

        {/* Выбор периода */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <div className="flex justify-center gap-2 rounded-xl bg-white p-2 shadow-sm">
            <Button
              variant={selectedPeriod === 'week' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setSelectedPeriod('week')}
            >
              Неделя
            </Button>
            <Button
              variant={selectedPeriod === 'month' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setSelectedPeriod('month')}
            >
              Месяц
            </Button>
            <Button
              variant={selectedPeriod === 'year' ? 'default' : 'ghost'}
              size="sm"
              onClick={() => setSelectedPeriod('year')}
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
          className="grid grid-cols-3 gap-4"
        >
          {/* Баланс */}
          <Card>
            <CardContent className="p-4">
              <div className="mb-2 flex items-center gap-2 text-purple-600">
                <Wallet className="h-4 w-4" />
                <p className="text-xs font-medium">Баланс</p>
              </div>
              <p className="text-xl font-bold text-gray-900">
                {formatCurrency(totalBalance, 'RUB')}
              </p>
            </CardContent>
          </Card>

          {/* Расходы */}
          <Card>
            <CardContent className="p-4">
              <div className="mb-2 flex items-center gap-2 text-red-600">
                <TrendingDown className="h-4 w-4" />
                <p className="text-xs font-medium">Расходы</p>
              </div>
              <p className="text-xl font-bold text-gray-900">
                {formatCurrency(expenses, 'RUB')}
              </p>
            </CardContent>
          </Card>

          {/* Доходы */}
          <Card>
            <CardContent className="p-4">
              <div className="mb-2 flex items-center gap-2 text-green-600">
                <TrendingUp className="h-4 w-4" />
                <p className="text-xs font-medium">Доходы</p>
              </div>
              <p className="text-xl font-bold text-gray-900">
                {formatCurrency(income, 'RUB')}
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
            <h3 className="mb-4 text-lg font-semibold text-gray-900">Топ категории расходов</h3>
            <div className="space-y-3">
              {topCategories.map((cat: any) => (
                <Card key={cat.category}>
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
              {categories.map((cat: any) => (
                <Card key={cat.category}>
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

        {/* Умные советы */}
        {expenseChange > 50 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="bg-gradient-to-r from-purple-50 to-blue-50">
              <CardContent className="p-4 flex items-start gap-3">
                <Lightbulb className="h-6 w-6 text-purple-600 flex-shrink-0" />
                <div>
                  <h3 className="mb-1 font-semibold text-gray-900">Умные советы</h3>
                  <p className="text-sm text-gray-700">
                    Ваши расходы составляют {((expenses / income) * 100).toFixed(0)}% от доходов. 
                    Рекомендуем откладывать минимум 20% дохода на сбережения.
                  </p>
                  {topCategories[0] && (
                    <p className="mt-2 text-sm text-gray-700">
                      Категория "{topCategories[0].categoryName}" занимает {topCategories[0].percentage}% расходов. 
                      Возможно, стоит пересмотреть траты в этой области.
                    </p>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Статистика */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          <h3 className="mb-4 text-lg font-semibold text-gray-900">Статистика</h3>
          {/* Placeholder для будущих графиков */}
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}

