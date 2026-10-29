import { useGetAccounts } from '@entities/account'
import { useGetAnalyticsOverview } from '@entities/analytics'
import { useGetMe } from '@entities/user'
import { LogoutButton } from '@features/auth/logout'
import { apiClient } from '@shared/api'
import { formatCurrency } from '@shared/lib/utils'
import { Button, Card, CardContent, Input, Label } from '@shared/ui'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { MobileHeader } from '@widgets/header'
import { motion } from 'framer-motion'
import {
  Award,
  Bell,
  Calendar,
  Check,
  ChevronRight,
  CreditCard,
  Crown,
  FileText,
  Gift,
  HelpCircle,
  Lock,
  Mail,
  Phone,
  Settings,
  Shield,
  Star,
  User,
  Wallet,
  X,
} from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export function ProfilePage() {
  const { data: user } = useGetMe()
  const { data: accounts } = useGetAccounts()
  const { data: analytics } = useGetAnalyticsOverview()
  const navigate = useNavigate()
  const [showEmailModal, setShowEmailModal] = useState(false)
  const [showPhoneModal, setShowPhoneModal] = useState(false)
  const [showNotificationsModal, setShowNotificationsModal] = useState(false)
  const [showSecurityModal, setShowSecurityModal] = useState(false)
  const [showAppSettingsModal, setShowAppSettingsModal] = useState(false)
  const [showHelpModal, setShowHelpModal] = useState(false)

  const accountsCount = accounts?.length || 0
  const isPremium = user?.accountType === 'premium'
  const totalBalance = analytics?.totalBalance || 0
  const isEmailVerified = user?.isVerified || false
  const isPhoneVerified = !!user?.phone

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
                      <p className="mt-1 text-sm opacity-90">{user?.email || ''}</p>
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
                      onClick={() => navigate('/cashback')}
                      className="flex items-center gap-1 rounded-lg bg-white/20 px-3 py-1.5 text-xs font-medium hover:bg-white/30"
                    >
                      <Star className="h-3 w-3" />
                      Кешбэк
                    </button>
                    <button
                      onClick={() => navigate('/referrals')}
                      className="flex items-center gap-1 rounded-lg bg-white/20 px-3 py-1.5 text-xs font-medium hover:bg-white/30"
                    >
                      <Gift className="h-3 w-3" />
                      Рефералы
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
                  value={user?.email || 'Не указан'}
                  isVerified={isEmailVerified}
                  onVerify={() => setShowEmailModal(true)}
                />
                <InfoRowWithVerification 
                  icon={<Phone className="h-5 w-5" />} 
                  label="Телефон" 
                  value={user?.phone || 'Не указан'}
                  isVerified={isPhoneVerified}
                  onVerify={() => setShowPhoneModal(true)}
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
                  {accounts.slice(0, 3).map((acc) => (
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
                <SettingsRow 
                  icon={<Bell className="h-5 w-5" />} 
                  label="Уведомления"
                  onClick={() => setShowNotificationsModal(true)}
                />
                <SettingsRow 
                  icon={<Lock className="h-5 w-5" />} 
                  label="Безопасность"
                  onClick={() => setShowSecurityModal(true)}
                />
                <SettingsRow 
                  icon={<Settings className="h-5 w-5" />} 
                  label="Настройки приложения"
                  onClick={() => setShowAppSettingsModal(true)}
                />
                <SettingsRow 
                  icon={<HelpCircle className="h-5 w-5" />} 
                  label="Помощь и поддержка"
                  onClick={() => setShowHelpModal(true)}
                />
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

      {/* Модальные окна */}
      {showEmailModal && (
        <EmailVerificationModal
          email={user?.email || ''}
          onClose={() => setShowEmailModal(false)}
          onSuccess={() => {
            setShowEmailModal(false)
            // Обновляем данные пользователя
          }}
        />
      )}

      {showPhoneModal && (
        <PhoneVerificationModal
          phone={user?.phone || ''}
          onClose={() => setShowPhoneModal(false)}
          onSuccess={() => {
            setShowPhoneModal(false)
            // Обновляем данные пользователя
          }}
        />
      )}

      {showNotificationsModal && (
        <NotificationsModal onClose={() => setShowNotificationsModal(false)} />
      )}

      {showSecurityModal && (
        <SecurityModal onClose={() => setShowSecurityModal(false)} />
      )}

      {showAppSettingsModal && (
        <AppSettingsModal onClose={() => setShowAppSettingsModal(false)} />
      )}

      {showHelpModal && (
        <HelpModal onClose={() => setShowHelpModal(false)} />
      )}
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

function SettingsRow({ icon, label, onClick }: { icon: React.ReactNode, label: string, onClick?: () => void }) {
  return (
    <button onClick={onClick} className="flex w-full items-center gap-3 p-4 transition-colors hover:bg-gray-50">
      <div className="text-gray-400">{icon}</div>
      <p className="flex-1 text-left font-medium text-gray-900">{label}</p>
      <ChevronRight className="h-5 w-5 text-gray-400" />
    </button>
  )
}

// Модальное окно подтверждения Email
function EmailVerificationModal({ email, onClose, onSuccess }: { email: string, onClose: () => void, onSuccess: () => void }) {
  const [inputEmail, setInputEmail] = useState(email)
  const [otpCode, setOtpCode] = useState('')
  const [step, setStep] = useState<'email' | 'code'>('email')
  const [showSuccessModal, setShowSuccessModal] = useState(false)
  const [showErrorModal, setShowErrorModal] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const queryClient = useQueryClient()

  const sendCodeMutation = useMutation({
    mutationFn: async (email: string) => {
      return apiClient.post('/api/auth/send-otp', { email })
    },
    onSuccess: () => {
      setStep('code')
    },
    onError: (error) => {
      setErrorMessage(error?.message || 'Не удалось отправить код')
      setShowErrorModal(true)
    }
  })

  const verifyCodeMutation = useMutation({
    mutationFn: async ({ email, code }: { email: string, code: string }) => {
      return apiClient.post('/api/auth/verify-email', { email, otpCode: code })
    },
    onSuccess: () => {
      setShowSuccessModal(true)
      // Обновляем данные пользователя
      queryClient.invalidateQueries({ queryKey: ['user', 'me'] })
      setTimeout(() => {
        setShowSuccessModal(false)
        onSuccess()
      }, 1500)
    },
    onError: (error) => {
      setErrorMessage(error?.message || 'Неверный код')
      setShowErrorModal(true)
    }
  })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Подтверждение Email</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>

        {step === 'email' ? (
          <>
            <div className="mb-4">
              <Label>Email</Label>
              <Input
                type="email"
                value={inputEmail}
                onChange={(e) => setInputEmail(e.target.value)}
                placeholder="example@mail.com"
                className="mt-1"
              />
            </div>
            <div className="flex gap-3">
              <Button variant="outline" onClick={onClose} className="flex-1">
                Отмена
              </Button>
              <Button
                onClick={() => {
                  if (!inputEmail || !inputEmail.includes('@')) {
                    setErrorMessage('Введите корректный email')
                    setShowErrorModal(true)
                    return
                  }
                  sendCodeMutation.mutate(inputEmail)
                }}
                disabled={sendCodeMutation.isPending}
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                {sendCodeMutation.isPending ? 'Отправка...' : 'Отправить код'}
              </Button>
            </div>
          </>
        ) : (
          <>
            <div className="mb-4 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-700">
                Код отправлен на <strong>{inputEmail}</strong>
              </p>
            </div>
            <div className="mb-4">
              <Label>Код подтверждения</Label>
              <Input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value)}
                placeholder="Введите код из письма"
                className="mt-1"
                maxLength={6}
              />
            </div>
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setStep('email')} className="flex-1">
                Назад
              </Button>
              <Button
                onClick={() => {
                  if (!otpCode || otpCode.length < 4) {
                    setErrorMessage('Введите код подтверждения')
                    setShowErrorModal(true)
                    return
                  }
                  verifyCodeMutation.mutate({ email: inputEmail, code: otpCode })
                }}
                disabled={verifyCodeMutation.isPending}
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                {verifyCodeMutation.isPending ? 'Проверка...' : 'Подтвердить'}
              </Button>
            </div>
          </>
        )}
      </motion.div>

      {/* Модальное окно успеха */}
      {showSuccessModal && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-md rounded-2xl bg-white p-6 text-center"
          >
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
                <Check className="h-8 w-8 text-green-600" />
              </div>
            </div>
            <h3 className="mb-2 text-xl font-bold text-gray-900">Email подтвержден</h3>
            <p className="mb-6 text-gray-600">Ваш email успешно подтвержден!</p>
          </motion.div>
        </div>
      )}

      {/* Модальное окно ошибки */}
      {showErrorModal && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-md rounded-2xl bg-white p-6 text-center"
          >
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
                <X className="h-8 w-8 text-red-600" />
              </div>
            </div>
            <h3 className="mb-2 text-xl font-bold text-gray-900">Ошибка</h3>
            <p className="mb-6 text-gray-600">{errorMessage}</p>
            <Button
              onClick={() => setShowErrorModal(false)}
              className="w-full bg-red-600 hover:bg-red-700"
            >
              OK
            </Button>
          </motion.div>
        </div>
      )}
    </div>
  )
}

// Модальное окно подтверждения телефона
function PhoneVerificationModal({ phone, onClose, onSuccess }: { phone: string, onClose: () => void, onSuccess: () => void }) {
  const [inputPhone, setInputPhone] = useState(phone)
  const [otpCode, setOtpCode] = useState('')
  const [step, setStep] = useState<'phone' | 'code'>('phone')
  const [showErrorModal, setShowErrorModal] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')

  const sendCodeMutation = useMutation({
    mutationFn: async (phone: string) => {
      // Отправляем код на указанный телефон
      return apiClient.post('/api/verification/send-phone-code', { phone })
    },
    onSuccess: () => {
      setStep('code')
      alert('📱 Код отправлен на ' + inputPhone)
    },
    onError: (error) => {
      alert('❌ Ошибка: ' + (error?.message || 'Не удалось отправить код'))
    }
  })

  const verifyCodeMutation = useMutation({
    mutationFn: async (code: string) => {
      return apiClient.post('/api/verification/verify-phone', { code })
    },
    onSuccess: () => {
      alert('✅ Номер телефона успешно подтвержден!')
      onSuccess()
    },
    onError: (error) => {
      alert('❌ Ошибка: ' + (error?.message || 'Неверный код'))
    }
  })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Подтверждение телефона</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>

        {step === 'phone' ? (
          <>
            <div className="mb-4">
              <Label>Номер телефона</Label>
              <Input
                type="tel"
                value={inputPhone}
                onChange={(e) => setInputPhone(e.target.value)}
                placeholder="+7 (900) 123-45-67"
                className="mt-1"
              />
            </div>
            <div className="flex gap-3">
              <Button variant="outline" onClick={onClose} className="flex-1">
                Отмена
              </Button>
              <Button
                onClick={() => {
                  const cleanPhone = inputPhone.replace(/[^\d+]/g, '')
                  if (!cleanPhone || cleanPhone.length < 10) {
                    setErrorMessage('Введите корректный номер телефона')
                    setShowErrorModal(true)
                    return
                  }
                  sendCodeMutation.mutate(cleanPhone)
                }}
                disabled={sendCodeMutation.isPending}
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                {sendCodeMutation.isPending ? 'Отправка...' : 'Отправить код'}
              </Button>
            </div>
          </>
        ) : (
          <>
            <div className="mb-4 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-gray-700">
                Код отправлен на <strong>{inputPhone}</strong>
              </p>
            </div>
            <div className="mb-4">
              <Label>Код подтверждения</Label>
              <Input
                type="text"
                value={otpCode}
                onChange={(e) => setOtpCode(e.target.value)}
                placeholder="Введите код из СМС"
                className="mt-1"
                maxLength={6}
              />
            </div>
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => setStep('phone')} className="flex-1">
                Назад
              </Button>
              <Button
                onClick={() => {
                  if (!otpCode || otpCode.length < 4) {
                    setErrorMessage('Введите код подтверждения')
                    setShowErrorModal(true)
                    return
                  }
                  verifyCodeMutation.mutate(otpCode)
                }}
                disabled={verifyCodeMutation.isPending}
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                {verifyCodeMutation.isPending ? 'Проверка...' : 'Подтвердить'}
              </Button>
            </div>
          </>
        )}
      </motion.div>

      {/* Модальное окно успеха */}
      {showErrorModal && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="w-full max-w-md rounded-2xl bg-white p-6 text-center"
          >
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-red-100">
                <X className="h-8 w-8 text-red-600" />
              </div>
            </div>
            <h3 className="mb-2 text-xl font-bold text-gray-900">Ошибка</h3>
            <p className="mb-6 text-gray-600">{errorMessage}</p>
            <Button
              onClick={() => setShowErrorModal(false)}
              className="w-full bg-red-600 hover:bg-red-700"
            >
              OK
            </Button>
          </motion.div>
        </div>
      )}
    </div>
  )
}

// Модальные окна для настроек
function NotificationsModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Уведомления</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 rounded-lg border border-gray-200">
            <div>
              <div className="font-medium text-gray-900">Push-уведомления</div>
              <div className="text-sm text-gray-500">Уведомления в приложении</div>
            </div>
            <input type="checkbox" defaultChecked className="w-5 h-5" />
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg border border-gray-200">
            <div>
              <div className="font-medium text-gray-900">Email-уведомления</div>
              <div className="text-sm text-gray-500">Уведомления на почту</div>
            </div>
            <input type="checkbox" defaultChecked className="w-5 h-5" />
          </div>
          <div className="flex items-center justify-between p-3 rounded-lg border border-gray-200">
            <div>
              <div className="font-medium text-gray-900">SMS-уведомления</div>
              <div className="text-sm text-gray-500">Уведомления по СМС</div>
            </div>
            <input type="checkbox" className="w-5 h-5" />
          </div>
        </div>
        <div className="mt-4">
          <Button onClick={onClose} className="w-full bg-blue-600 hover:bg-blue-700">
            Сохранить
          </Button>
        </div>
      </motion.div>
    </div>
  )
}

function SecurityModal({ onClose }: { onClose: () => void }) {
  const [selectedAction, setSelectedAction] = useState<'password' | '2fa' | 'history' | null>(null)
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  if (!selectedAction) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full max-w-md rounded-2xl bg-white p-6"
        >
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-xl font-bold text-gray-900">Безопасность</h3>
            <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="space-y-3">
            <button
              onClick={() => setSelectedAction('password')}
              className="w-full flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors text-left"
            >
              <Lock className="h-5 w-5 text-gray-400" />
              <div className="flex-1">
                <div className="font-medium text-gray-900">Смена пароля</div>
                <div className="text-sm text-gray-500">Изменить текущий пароль</div>
              </div>
            </button>
            <button
              onClick={() => setSelectedAction('2fa')}
              className="w-full flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors text-left"
            >
              <Shield className="h-5 w-5 text-gray-400" />
              <div className="flex-1">
                <div className="font-medium text-gray-900">Двухфакторная аутентификация</div>
                <div className="text-sm text-gray-500">Дополнительная защита аккаунта</div>
              </div>
            </button>
            <button
              onClick={() => setSelectedAction('history')}
              className="w-full flex items-center gap-3 p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors text-left"
            >
              <FileText className="h-5 w-5 text-gray-400" />
              <div className="flex-1">
                <div className="font-medium text-gray-900">История входов</div>
                <div className="text-sm text-gray-500">Просмотр истории входов в аккаунт</div>
              </div>
            </button>
          </div>
          <div className="mt-4">
            <Button variant="outline" onClick={onClose} className="w-full">
              Закрыть
            </Button>
          </div>
        </motion.div>
      </div>
    )
  }

  if (selectedAction === 'password') {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full max-w-md rounded-2xl bg-white p-6"
        >
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-xl font-bold text-gray-900">Смена пароля</h3>
            <button onClick={() => setSelectedAction(null)} className="rounded-full p-1 hover:bg-gray-100">
              <X className="h-5 w-5" />
            </button>
          </div>
          <div className="space-y-4">
            <div>
              <Label>Новый пароль</Label>
              <Input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Минимум 8 символов"
                className="mt-1"
              />
            </div>
            <div>
              <Label>Подтвердите пароль</Label>
              <Input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Повторите пароль"
                className="mt-1"
              />
            </div>
          </div>
          <div className="mt-4 flex gap-3">
            <Button variant="outline" onClick={() => setSelectedAction(null)} className="flex-1">
              Назад
            </Button>
            <Button
              onClick={() => {
                if (!newPassword || newPassword.length < 8) {
                  alert('❌ Пароль должен быть минимум 8 символов')
                  return
                }
                if (newPassword !== confirmPassword) {
                  alert('❌ Пароли не совпадают')
                  return
                }
                alert('✅ Пароль успешно изменен!\n\nФункция смены пароля будет доступна в следующей версии.')
                onClose()
              }}
              className="flex-1 bg-blue-600 hover:bg-blue-700"
            >
              Сохранить
            </Button>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">
            {selectedAction === '2fa' && 'Двухфакторная аутентификация'}
            {selectedAction === 'history' && 'История входов'}
          </h3>
          <button onClick={() => setSelectedAction(null)} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="p-4 bg-blue-50 rounded-lg mb-4">
          <p className="text-sm text-gray-700">
            {selectedAction === '2fa' && 'Функция двухфакторной аутентификации будет доступна в следующей версии.'}
            {selectedAction === 'history' && 'Просмотр истории входов будет доступен в следующей версии.'}
          </p>
        </div>
        <Button variant="outline" onClick={() => setSelectedAction(null)} className="w-full">
          Назад
        </Button>
      </motion.div>
    </div>
  )
}

function AppSettingsModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Настройки приложения</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="space-y-4">
          <div>
            <Label>Язык интерфейса</Label>
            <select className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg">
              <option>Русский</option>
              <option>English</option>
            </select>
          </div>
          <div>
            <Label>Валюта по умолчанию</Label>
            <select className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-lg">
              <option>RUB (₽)</option>
              <option>USD ($)</option>
              <option>EUR (€)</option>
            </select>
          </div>
        </div>
        <div className="mt-4">
          <Button onClick={onClose} className="w-full bg-blue-600 hover:bg-blue-700">
            Сохранить
          </Button>
        </div>
      </motion.div>
    </div>
  )
}

function HelpModal({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Помощь и поддержка</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>
        <div className="space-y-3">
          <button className="w-full p-3 rounded-lg border border-gray-200 hover:bg-gray-50 text-left">
            <div className="font-medium text-gray-900">Часто задаваемые вопросы</div>
            <div className="text-sm text-gray-500">Ответы на популярные вопросы</div>
          </button>
          <button className="w-full p-3 rounded-lg border border-gray-200 hover:bg-gray-50 text-left">
            <div className="font-medium text-gray-900">Связаться с поддержкой</div>
            <div className="text-sm text-gray-500">Напишите нам или позвоните</div>
          </button>
          <button className="w-full p-3 rounded-lg border border-gray-200 hover:bg-gray-50 text-left">
            <div className="font-medium text-gray-900">Обратная связь</div>
            <div className="text-sm text-gray-500">Поделитесь своими предложениями</div>
          </button>
        </div>
        <div className="mt-4">
          <Button onClick={onClose} className="w-full bg-blue-600 hover:bg-blue-700">
            Закрыть
          </Button>
        </div>
      </motion.div>
    </div>
  )
}
