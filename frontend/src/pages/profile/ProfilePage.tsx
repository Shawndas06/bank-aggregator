import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { LogoutButton } from '@features/auth/logout'
import { useGetMe } from '@entities/user'
import { User } from 'lucide-react'

export function ProfilePage() {
  const { data: user } = useGetMe()

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
          <h2 className="mb-2 text-2xl font-bold text-gray-900">Профиль</h2>
          <p className="text-gray-600">Управление вашим аккаунтом</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="space-y-6"
        >
          {/* User Info Card */}
          <div className="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
            <div className="mb-4 flex items-center gap-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-r from-purple-600 to-blue-600">
                <User className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {user?.name || 'Загрузка...'}
                </h3>
                <p className="text-sm text-gray-600">{user?.email || ''}</p>
              </div>
            </div>
          </div>

          {/* Logout Button */}
          <div className="pt-4">
            <LogoutButton variant="outline" />
          </div>
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}
