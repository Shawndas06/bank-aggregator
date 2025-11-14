import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { LogoutButton } from '@features/auth/logout'
import { useGetMe } from '@entities/user'
import { useGetAccounts } from '@entities/account'
import { useGetAnalyticsOverview } from '@entities/analytics'
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
  HelpCircle,
  Check,
  X,
  FileText,
  Gift,
  TrendingUp,
  Wallet,
  Star,
  Award
} from 'lucide-react'
import { Card, CardContent, Button } from '@shared/ui'
import { formatCurrency } from '@shared/lib/utils'
import { useNavigate } from 'react-router-dom'

export function ProfilePage() {
  const { data: user } = useGetMe()
  const { data: accounts } = useGetAccounts()
  const { data: analytics } = useGetAnalyticsOverview()
  const navigate = useNavigate()

  const accountsCount = accounts?.length || 0
  const isPremium = user?.accountType === 'premium'
  const totalBalance = analytics?.totalBalance || 0
  const isEmailVerified = false // TODO: Add email verification to API
  const isPhoneVerified = false // TODO: Add phone verification to API

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6 space-y-4">
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
          <Card className="border-0 bg-gradient-to-r from-purple-600 via-purple-500 to-blue-600 text-white shadow-xl">
            <CardContent className="p-6">
              <div className="flex items-start gap-4">
                <div className="flex h-20 w-20 flex-shrink-0 items-center justify-center rounded-full border-4 border-white/30 bg-white/20 backdrop-blur-sm">
                  <User className="h-10 w-10 text-white" />
                </div>
                <div className="flex-1">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-xl font-bold">
                        {user?.name || 'Загрузка...'}
                      </h3>
                      <p className="mt-1 text-sm opacity-90">{user?.name || ''}</p>
                    </div>
                    {isPremium && (
                      <div className="rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 px-3 py-1">
                        <div className="flex items-center gap-1">
                          <Crown className="h-3 w-3 text-white" />
                          <span className="text-xs font-bold text-white">Premium</span>
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="mt-3 flex items-center gap-4">
                    <button
                      onClick={() => navigate('/premium')}
                      className="flex items-center gap-1 rounded-lg bg-white/20 px-3 py-1.5 text-xs font-medium hover:bg-white/30"
                    >
                      <Gift className="h-3 w-3" />
                      {isPremium ? 'Управление подпиской' : 'Получить Premium'}
                    </button>
                    <button
                      onClick={() => alert('🎁 Ваш кешбэк: 0 ₽\n\n• Делайте покупки\n• Получайте кешбэк\n• Выводите на счет')}
                      className="flex items-center gap-1 rounded-lg bg-white/20 px-3 py-1.5 text-xs font-medium hover:bg-white/30"
                    >
                      <Star className="h-3 w-3" />
                      Кешбэк
                    </button>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Stats - 3 карточки как в Альфа/Тинькофф */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="grid grid-cols-3 gap-3"
        >
          <Card className="bg-gradient-to-br from-purple-50 to-purple-100">
            <CardContent className="p-4 text-center">
              <Wallet className="mx-auto mb-2 h-6 w-6 text-purple-600" />
              <p className="text-lg font-bold text-purple-600">
                {formatCurrency(totalBalance, 'RUB').split(',')[0]}
              </p>
              <p className="text-xs font-medium text-gray-600">Баланс</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-blue-50 to-blue-100">
            <CardContent className="p-4 text-center">
              <CreditCard className="mx-auto mb-2 h-6 w-6 text-blue-600" />
              <p className="text-lg font-bold text-blue-600">{accountsCount}</p>
              <p className="text-xs font-medium text-gray-600">Счетов</p>
            </CardContent>
          </Card>
          <Card className="bg-gradient-to-br from-green-50 to-green-100">
            <CardContent className="p-4 text-center">
              <Shield className="mx-auto mb-2 h-6 w-6 text-green-600" />
              <p className="text-lg font-bold text-green-600">
                {isEmailVerified && isPhoneVerified ? '100%' : '50%'}
              </p>
              <p className="text-xs font-medium text-gray-600">Защита</p>
            </CardContent>
          </Card>
        </motion.div>

        {/* Personal Info - как в Сбере с галочками */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <h3 className="mb-3 text-lg font-semibold text-gray-900">Личная информация</h3>
          <Card>
            <CardContent className="p-0">
              <div className="divide-y divide-gray-100">
                <InfoRowWithVerification 
                  icon={<Mail className="h-5 w-5" />} 
                  label="Email" 
                  value="Не указан"
                  isVerified={isEmailVerified}
                  onVerify={() => alert('📧 Код отправлен')}
                />
                <InfoRowWithVerification 
                  icon={<Phone className="h-5 w-5" />} 
                  label="Телефон" 
                  value="Не указан"
                  isVerified={isPhoneVerified}
                  onVerify={() => alert('📱 СМС отправлена')}
                />
                <InfoRow 
                  icon={<Calendar className="h-5 w-5" />} 
                  label="Дата рождения" 
                  value={user?.birthDate ? new Date(user.birthDate).toLocaleDateString('ru-RU') : 'Не указана'} 
                />
                <InfoRow 
                  icon={<Award className="h-5 w-5" />} 
                  label="Статус" 
                  value={isPremium ? 'Premium клиент' : 'Базовый тариф'} 
                />
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Мои продукты - как в ВТБ */}
        {accounts && accounts.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.5 }}
          >
            <h3 className="mb-3 text-lg font-semibold text-gray-900">Мои продукты</h3>
            <Card>
              <CardContent className="p-4">
                <div className="space-y-3">
                  {accounts.slice(0, 3).map((acc: any) => (
                    <div 
                      key={`${acc.clientId}-${acc.accountId}`} 
                      className="flex items-center justify-between"
                    >
                      <div className="flex items-center gap-3">
                        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100">
                          <CreditCard className="h-5 w-5 text-blue-600" />
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">{acc.accountName}</p>
                          <p className="text-xs text-gray-500">{acc.clientName}</p>
                        </div>
                      </div>
                      <ChevronRight className="h-5 w-5 text-gray-400" />
                    </div>
                  ))}
                </div>
                {accounts.length > 3 && (
                  <button
                    onClick={() => navigate('/accounts')}
                    className="mt-3 w-full rounded-lg bg-gray-50 py-2 text-sm font-medium text-purple-600 hover:bg-gray-100"
                  >
                    Показать все ({accounts.length})
                  </button>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}

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

function InfoRowWithVerification({ icon, label, value, isVerified, onVerify }: { icon: React.ReactNode, label: string, value: string, isVerified: boolean, onVerify?: () => void }) {
  const handleVerify = () => {
    if (onVerify) {
      onVerify()
    } else if (label === 'Email') {
      alert('📧 Подтверждение Email\n\nПисьмо с кодом отправлено на вашу почту.\nВведите код для подтверждения.')
    } else if (label === 'Телефон') {
      alert('📱 Подтверждение номера\n\nСМС с кодом отправлена на ваш номер.\nВведите код для подтверждения.')
    }
  }

  return (
    <div className="flex items-center gap-3 p-4">
      <div className="text-gray-400">{icon}</div>
      <div className="flex-1">
        <p className="text-sm text-gray-600">{label}</p>
        <p className="font-medium text-gray-900">{value}</p>
      </div>
      {isVerified ? (
        <div className="flex items-center gap-1 rounded-full bg-green-100 px-2 py-1">
          <Check className="h-3 w-3 text-green-600" />
          <span className="text-xs font-medium text-green-600">Подтвержден</span>
        </div>
      ) : (
        <button
          onClick={handleVerify}
          className="flex items-center gap-1 rounded-full bg-orange-100 px-2 py-1 transition-all hover:bg-orange-200 active:scale-95"
        >
          <X className="h-3 w-3 text-orange-600" />
          <span className="text-xs font-medium text-orange-600">Подтвердить</span>
        </button>
      )}
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
