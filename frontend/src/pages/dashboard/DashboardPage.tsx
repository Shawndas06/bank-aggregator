import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { AnalyticsCards } from '@widgets/analytics-cards'
import { TransactionsList } from '@widgets/transactions-list'
import { AccountList } from '@widgets/account-list'
import { useGetAccounts } from '@entities/account'
import { Plus, QrCode, Gift, TrendingUp } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function DashboardPage() {
  const { data: accounts } = useGetAccounts()
  const navigate = useNavigate()

  if (!accounts?.length) {
    return (
      <div className="min-h-screen bg-gray-50 pb-20">
        <MobileHeader />
        <main className="container mx-auto px-4 py-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <AccountList />
          </motion.div>
        </main>
        <BottomNavigation />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6 space-y-6">
        {/* Заголовок */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="mb-2 text-2xl font-bold text-gray-900">Главная</h2>
          <p className="text-gray-600">Обзор ваших финансов</p>
        </motion.div>

        {/* Быстрые действия */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
        >
          <div className="grid grid-cols-4 gap-3">
            <QuickActionCard 
              icon={<TrendingUp className="h-6 w-6" />} 
              label="Аналитика" 
              onClick={() => navigate('/analytics')} 
            />
            <QuickActionCard 
              icon={<QrCode className="h-6 w-6" />} 
              label="QR" 
              onClick={() => alert('🔜 QR-платежи будут доступны в следующей версии!')} 
            />
            <QuickActionCard 
              icon={<Gift className="h-6 w-6" />} 
              label="Подарки" 
              onClick={() => navigate('/loyalty-cards')} 
            />
            <QuickActionCard 
              icon={<Plus className="h-6 w-6" />} 
              label="Еще" 
              onClick={() => alert('🔜 Дополнительные функции в разработке!')} 
            />
          </div>
        </motion.div>

        {/* Аналитика */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <AnalyticsCards />
        </motion.div>

        {/* Последние транзакции */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <h3 className="mb-4 text-lg font-semibold text-gray-900">Последние транзакции</h3>
          <TransactionsList />
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}

type QuickActionCardProps = {
  icon: React.ReactNode
  label: string
  onClick?: () => void
}

function QuickActionCard({ icon, label, onClick }: QuickActionCardProps) {
  return (
    <button
      onClick={onClick}
      className="flex flex-col items-center justify-center gap-2 rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition-all hover:scale-105 hover:shadow-md active:scale-95"
    >
      <div className="text-purple-600">{icon}</div>
      <span className="text-xs font-medium text-gray-700">{label}</span>
    </button>
  )
}


