import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { useGetMe } from '@entities/user'
import { Button, Card, CardContent } from '@shared/ui'
import { Crown, Check, Zap, Users, BarChart, Headphones, ArrowLeft } from 'lucide-react'

export function PremiumPage() {
  const navigate = useNavigate()
  const { data: user } = useGetMe()
  const [isProcessing, setIsProcessing] = useState(false)

  const isPremium = user?.accountType === 'premium'

  const features = [
    {
      icon: Users,
      title: 'До 5 групп',
      description: 'Создавайте множество групп для разных целей',
      free: '1 группа',
      premium: '5 групп',
    },
    {
      icon: Users,
      title: 'До 20 участников',
      description: 'Добавляйте больше участников в каждую группу',
      free: '2 участника',
      premium: '20 участников',
    },
    {
      icon: BarChart,
      title: 'Расширенная аналитика',
      description: 'Подробные отчеты и графики по всем счетам',
      free: '—',
      premium: '✓',
    },
    {
      icon: Headphones,
      title: 'Приоритетная поддержка',
      description: 'Быстрые ответы на все ваши вопросы',
      free: '—',
      premium: '✓',
    },
  ]

  const handlePurchase = async () => {
    setIsProcessing(true)
    // TODO: Implement actual payment integration
    setTimeout(() => {
      alert('Функция оплаты будет реализована позже')
      setIsProcessing(false)
    }, 1000)
  }

  if (isPremium) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        <MobileHeader />
        <main className="container mx-auto px-4 py-6">
          <button
            onClick={() => navigate(-1)}
            className="mb-4 flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-4 w-4" />
            Назад
          </button>

          <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
            <div className="mb-6 flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-purple-600 to-blue-600">
              <Crown className="h-12 w-12 text-white" />
            </div>
            <h2 className="mb-2 text-2xl font-bold text-gray-900">Вы уже Premium!</h2>
            <p className="text-gray-600">Наслаждайтесь всеми преимуществами подписки</p>
          </div>
        </main>
        <BottomNavigation />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 to-blue-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6">
        <button
          onClick={() => navigate(-1)}
          className="mb-4 flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4" />
          Назад
        </button>

        {/* Hero Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-8 text-center"
        >
          <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-purple-600 to-blue-600">
            <Crown className="h-8 w-8 text-white" />
          </div>
          <h1 className="mb-2 text-3xl font-bold text-gray-900">Станьте Premium</h1>
          <p className="text-gray-600">Получите полный доступ ко всем возможностям сервиса</p>
        </motion.div>

        {/* Pricing Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="mb-8"
        >
          <Card className="border-0 bg-gradient-to-br from-purple-600 to-blue-600 shadow-2xl">
            <CardContent className="p-6 text-white">
              <div className="mb-4 flex items-center justify-between">
                <div>
                  <p className="text-sm opacity-90">Premium подписка</p>
                  <div className="mt-1 flex items-baseline gap-2">
                    <span className="text-5xl font-bold">299 ₽</span>
                    <span className="text-lg opacity-75">/ месяц</span>
                  </div>
                </div>
                <Zap className="h-12 w-12 opacity-75" />
              </div>
              <p className="mb-6 text-sm opacity-90">
                Подписка продлевается автоматически. Отменить можно в любой момент.
              </p>
              <Button
                onClick={handlePurchase}
                disabled={isProcessing}
                className="w-full bg-white py-6 text-lg font-semibold text-purple-600 shadow-lg hover:bg-gray-50"
              >
                {isProcessing ? 'Обработка...' : 'Оформить подписку'}
              </Button>
            </CardContent>
          </Card>
        </motion.div>

        {/* Features Comparison */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="mb-8"
        >
          <h2 className="mb-4 text-xl font-bold text-gray-900">Что вы получите</h2>
          <div className="space-y-3">
            {features.map((feature, index) => {
              const Icon = feature.icon
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 + index * 0.1, duration: 0.5 }}
                >
                  <Card>
                    <CardContent className="p-4">
                      <div className="mb-3 flex items-start gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                          <Icon className="h-5 w-5 text-blue-600" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900">{feature.title}</h3>
                          <p className="text-sm text-gray-600">{feature.description}</p>
                        </div>
                      </div>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="rounded-lg bg-gray-100 p-3">
                          <p className="mb-1 text-xs font-medium text-gray-500">Free</p>
                          <p className="text-sm font-semibold text-gray-700">{feature.free}</p>
                        </div>
                        <div className="rounded-lg bg-gradient-to-br from-purple-100 to-blue-100 p-3">
                          <p className="mb-1 text-xs font-medium text-purple-700">Premium</p>
                          <p className="text-sm font-semibold text-purple-900">{feature.premium}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              )
            })}
          </div>
        </motion.div>

        {/* Benefits */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
        >
          <Card className="border-green-200 bg-green-50">
            <CardContent className="p-4">
              <h3 className="mb-3 font-semibold text-gray-900">Почему стоит попробовать?</h3>
              <ul className="space-y-2">
                {[
                  'Отменить подписку можно в любой момент',
                  'Безопасная оплата',
                  'Моментальная активация',
                  'Техподдержка 24/7',
                ].map((benefit, index) => (
                  <li key={index} className="flex items-center gap-2 text-sm text-gray-700">
                    <div className="flex h-5 w-5 items-center justify-center rounded-full bg-green-200">
                      <Check className="h-3 w-3 text-green-700" />
                    </div>
                    {benefit}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}
