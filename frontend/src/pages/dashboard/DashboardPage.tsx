import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { DashboardSummary } from '@widgets/dashboard-summary'
import { AccountList } from '@widgets/account-list'
import { useGetAccounts } from '@entities/account'

export function DashboardPage() {
  const { data: accounts } = useGetAccounts()

  return (
    <div className="min-h-screen bg-gray-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-6"
        >
          <h2 className="mb-2 text-2xl font-bold text-gray-900">Главная</h2>
          <p className="text-gray-600">Обзор ваших финансов</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          {!accounts?.length ? <AccountList /> : <DashboardSummary />}
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}
