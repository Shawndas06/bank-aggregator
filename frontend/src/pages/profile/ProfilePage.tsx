import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { LogoutButton } from '@features/auth/logout'
import { useGetMe } from '@entities/user'
import { useGetAccounts } from '@entities/account'
import { 
  User, 
  Mail, 
  Phone, 
  Calendar, 
  Shield, 
  Bell, 
  Lock, 
  CreditCard,
  ChevronRight,
  Crown,
  Settings,
  HelpCircle
} from 'lucide-react'
import { Card, CardContent } from '@shared/ui'

export function ProfilePage() {
  const { data: user } = useGetMe()
  const { data: accounts } = useGetAccounts()

  const accountsCount = accounts?.length || 0
  const isPremium = user?.accountType === 'PREMIUM'

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6 space-y-6">
        {/* Заголовок */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="mb-2 text-2xl font-bold text-gray-900">Профиль</h2>
          <p className="text-gray-600">Управление вашим аккаунтом</p>
        </motion.div>

        {/* User Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
        >
          <Card className="border-0 bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg">
            <CardContent className="p-6">
              <div className="flex items-center gap-4">
                <div className="flex h-20 w-20 items-center justify-center rounded-full bg-white/20 backdrop-blur">
                  <User className="h-10 w-10 text-white" />
                </div>
                <div className="flex-1">
                  <h3 className="text-xl font-bold">
                    {user?.name || 'Загрузка...'}
                  </h3>
                  <p className="mt-1 text-sm opacity-90">{user?.email || ''}</p>
                  {isPremium && (
                    <div className="mt-2 inline-flex items-center gap-1 rounded-full bg-yellow-400/20 px-3 py-1 text-xs font-semibold text-yellow-100">
                      <Crown className="h-3 w-3" />
                      Premium
                    </div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="grid grid-cols-2 gap-4"
        >
          <Card className="bg-gradient-to-br from-purple-50 to-blue-50">
            <CardContent className="p-4 text-center">
              <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100">
                <CreditCard className="h-6 w-6 text-purple-600" />
              </div>
              <p className="text-2xl font-bold text-purple-600">{accountsCount}</p>
              <p className="text-sm font-medium text-gray-700">Счетов</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-green-50 to-emerald-50">
            <CardContent className="p-4 text-center">
              <div className="mx-auto mb-2 flex h-12 w-12 items-center justify-center rounded-full bg-green-100">
                <Shield className="h-6 w-6 text-green-600" />
              </div>
              <p className="text-2xl font-bold text-green-600">100%</p>
              <p className="text-sm font-medium text-gray-700">Безопасность</p>
            </CardContent>
          </Card>
        </motion.div>

        {/* Personal Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <h3 className="mb-3 text-lg font-semibold text-gray-900">Личная информация</h3>
          <Card>
            <CardContent className="p-0">
              <div className="divide-y divide-gray-100">
                <InfoRow icon={<Mail className="h-5 w-5" />} label="Email" value={user?.email || 'Не указан'} />
                <InfoRow icon={<Phone className="h-5 w-5" />} label="Телефон" value={user?.phone || 'Не указан'} />
                <InfoRow 
                  icon={<Calendar className="h-5 w-5" />} 
                  label="Дата рождения" 
                  value={user?.birthDate ? new Date(user.birthDate).toLocaleDateString('ru-RU') : 'Не указана'} 
                />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Settings */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.5 }}
        >
          <h3 className="mb-3 text-lg font-semibold text-gray-900">Настройки</h3>
          <Card>
            <CardContent className="p-0">
              <div className="divide-y divide-gray-100">
                <SettingsRow icon={<Bell className="h-5 w-5" />} label="Уведомления" />
                <SettingsRow icon={<Lock className="h-5 w-5" />} label="Безопасность" />
                <SettingsRow icon={<Settings className="h-5 w-5" />} label="Настройки приложения" />
                <SettingsRow icon={<HelpCircle className="h-5 w-5" />} label="Помощь и поддержка" />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Logout Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="pt-2"
        >
          <LogoutButton variant="outline" />
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}

function InfoRow({ icon, label, value }: { icon: React.ReactNode, label: string, value: string }) {
  return (
    <div className="flex items-center gap-3 p-4">
      <div className="text-gray-400">{icon}</div>
      <div className="flex-1">
        <p className="text-sm text-gray-600">{label}</p>
        <p className="font-medium text-gray-900">{value}</p>
      </div>
    </div>
  )
}

function SettingsRow({ icon, label }: { icon: React.ReactNode, label: string }) {
  return (
    <button className="flex w-full items-center gap-3 p-4 transition-colors hover:bg-gray-50">
      <div className="text-gray-400">{icon}</div>
      <p className="flex-1 text-left font-medium text-gray-900">{label}</p>
      <ChevronRight className="h-5 w-5 text-gray-400" />
    </button>
  )
}
