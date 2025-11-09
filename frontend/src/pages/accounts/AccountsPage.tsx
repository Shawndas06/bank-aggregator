import { useState } from 'react'
import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { AccountList } from '@widgets/account-list'
import { Button, Card, CardContent, Input, Label } from '@shared/ui'
import { useGetAccounts } from '@entities/account'
import { apiClient } from '@shared/api'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  CreditCard, 
  Gift, 
  Plus, 
  Eye, 
  EyeOff, 
  ArrowUpDown,
  Sparkles,
  X
} from 'lucide-react'

type ModalType = 'create-account' | 'loyalty-cards' | 'set-priority' | null

export function AccountsPage() {
  const { data: accounts } = useGetAccounts()
  const [activeModal, setActiveModal] = useState<ModalType>(null)
  const queryClient = useQueryClient()

  return (
    <div className="min-h-screen pb-20" style={{ background: 'linear-gradient(135deg, #DBEAFE 0%, #FFFFFF 50%, #E0E7FF 100%)' }}>
      <MobileHeader />

      <main className="container mx-auto px-4 py-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="mb-2 text-3xl font-bold" style={{ background: 'linear-gradient(90deg, #3B82F6 0%, #6366F1 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            Счета
          </h2>
          <p className="text-gray-700 text-base font-medium">Управление банковскими счетами</p>
        </motion.div>

        {/* Быстрые действия */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="my-4 grid grid-cols-4 gap-3"
        >
          <ActionButton
            icon={<Plus className="h-5 w-5" />}
            label="Создать счет"
            color="blue"
            onClick={() => setActiveModal('create-account')}
          />
          <ActionButton
            icon={<Gift className="h-5 w-5" />}
            label="Лояльность"
            color="pink"
            onClick={() => setActiveModal('loyalty-cards')}
          />
          <ActionButton
            icon={<ArrowUpDown className="h-5 w-5" />}
            label="Приоритеты"
            color="purple"
            onClick={() => setActiveModal('set-priority')}
          />
          <ActionButton
            icon={<Sparkles className="h-5 w-5" />}
            color="green"
            label="Настройки"
            onClick={() => alert('⚙️ Настройки счетов:\n\n• Переименование\n• Синхронизация\n• Скрытие балансов\n\nДоступно в меню каждого счета')}
          />
        </motion.div>

        {/* Список счетов */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <AccountList />
        </motion.div>
      </main>

      <BottomNavigation />

      {/* Модальные окна */}
      {activeModal === 'create-account' && (
        <CreateAccountModal
          onClose={() => setActiveModal(null)}
          onSuccess={() => {
            setActiveModal(null)
            queryClient.invalidateQueries(['accounts'])
          }}
        />
      )}

      {activeModal === 'loyalty-cards' && (
        <LoyaltyCardsModal
          onClose={() => setActiveModal(null)}
        />
      )}

      {activeModal === 'set-priority' && (
        <SetPriorityModal
          accounts={accounts || []}
          onClose={() => setActiveModal(null)}
          onSuccess={() => {
            setActiveModal(null)
            queryClient.invalidateQueries(['accounts'])
          }}
        />
      )}
    </div>
  )
}
// Кнопка быстрого действия
const actionButtonColors = {
  blue: 'bg-gradient-to-br from-blue-500 to-blue-600 shadow-blue-500/30',
  purple: 'bg-gradient-to-br from-purple-500 to-purple-600 shadow-purple-500/30',
  pink: 'bg-gradient-to-br from-pink-500 to-rose-500 shadow-pink-500/30',
  green: 'bg-gradient-to-br from-green-500 to-emerald-600 shadow-green-500/30',
  default: 'bg-gradient-to-br from-gray-500 to-gray-600 shadow-gray-500/30',
}

const actionButtonInlineStyles = {
  blue: { background: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)', boxShadow: '0 4px 12px rgba(59, 130, 246, 0.3)' },
  purple: { background: 'linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%)', boxShadow: '0 4px 12px rgba(139, 92, 246, 0.3)' },
  pink: { background: 'linear-gradient(135deg, #EC4899 0%, #DB2777 100%)', boxShadow: '0 4px 12px rgba(236, 72, 153, 0.3)' },
  green: { background: 'linear-gradient(135deg, #10B981 0%, #059669 100%)', boxShadow: '0 4px 12px rgba(16, 185, 129, 0.3)' },
  default: { background: 'linear-gradient(135deg, #6B7280 0%, #4B5563 100%)', boxShadow: '0 4px 12px rgba(107, 114, 128, 0.3)' },
}

function ActionButton({ icon, label, color = 'default', onClick }: { icon: React.ReactNode, label: string, color?: keyof typeof actionButtonInlineStyles, onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      style={actionButtonInlineStyles[color]}
      className="flex flex-col items-center gap-1.5 rounded-2xl p-3 text-white transition-all duration-300 hover:scale-105 active:scale-95"
    >
      <div className="text-white">{icon}</div>
      <span className="text-[10px] font-semibold text-center leading-tight">{label}</span>
    </button>
  )
}

// Модалка создания счета
function CreateAccountModal({ onClose, onSuccess }: { onClose: () => void, onSuccess: () => void }) {
  const [selectedBank, setSelectedBank] = useState<number>(1)
  const [accountName, setAccountName] = useState('')
  const [initialBalance, setInitialBalance] = useState('')

  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      return apiClient.post('/api/accounts/create-direct', {
        clientId: data.bankId,
        accountName: data.accountName,
        initialBalance: data.initialBalance
      })
    },
    onSuccess: (data: any) => {
      const accountName = data?.account?.accountName || 'счет'
      alert(`✅ Успешно!\n\n${accountName} создан и готов к использованию!`)
      onSuccess()
    },
    onError: (error: any) => {
      alert(`❌ Ошибка создания счета\n\n${error?.message || 'Попробуйте позже'}`)
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!accountName.trim()) {
      alert('❌ Укажите название счета')
      return
    }

    if (accountName.trim().length < 3) {
      alert('❌ Название должно содержать минимум 3 символа')
      return
    }

    const balance = parseFloat(initialBalance) || 0
    if (balance < 0) {
      alert('❌ Начальный баланс не может быть отрицательным')
      return
    }

    if (balance > 10000000) {
      alert('❌ Максимальный начальный баланс: 10 000 000 ₽')
      return
    }

    createMutation.mutate({
      bankId: selectedBank,
      accountName: accountName.trim(),
      initialBalance: balance
    })
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Создать новый счет</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <Label>Банк</Label>
            <select
              value={selectedBank}
              onChange={(e) => setSelectedBank(parseInt(e.target.value))}
              className="w-full rounded-lg border border-gray-300 px-3 py-2"
            >
              <option value={1}>VBank</option>
              <option value={3}>ABank</option>
              <option value={2}>SBank</option>
            </select>
          </div>

          <div>
            <Label>Название счета</Label>
            <Input
              type="text"
              placeholder="Например: Накопительный счет"
              value={accountName}
              onChange={(e) => setAccountName(e.target.value)}
            />
          </div>

          <div>
            <Label>Начальный баланс (₽)</Label>
            <Input
              type="number"
              placeholder="10000"
              value={initialBalance}
              onChange={(e) => setInitialBalance(e.target.value)}
            />
          </div>

          <div className="flex gap-3 pt-2">
            <Button type="button" variant="outline" onClick={onClose} className="flex-1">
              Отмена
            </Button>
            <Button
              type="submit"
              disabled={createMutation.isPending}
              className="flex-1 bg-purple-600 hover:bg-purple-700"
            >
              {createMutation.isPending ? 'Создание...' : 'Создать'}
            </Button>
          </div>
        </form>
      </motion.div>
    </div>
  )
}

// Модалка карт лояльности
function LoyaltyCardsModal({ onClose }: { onClose: () => void }) {
  const [cards, setCards] = useState<any[]>([])
  const [showAddForm, setShowAddForm] = useState(false)
  const [formData, setFormData] = useState({
    cardType: 'MAGNIT',
    cardNumber: '',
    cardName: ''
  })
  const queryClient = useQueryClient()

  // Загрузка карт
  const { data: cardsData } = useQuery({
    queryKey: ['loyalty-cards'],
    queryFn: () => apiClient.get('/api/loyalty-cards')
  })

  const addCardMutation = useMutation({
    mutationFn: (data: any) => apiClient.post('/api/loyalty-cards', data),
    onSuccess: () => {
      alert('✅ Карта добавлена!')
      queryClient.invalidateQueries(['loyalty-cards'])
      setShowAddForm(false)
      setFormData({ cardType: 'MAGNIT', cardNumber: '', cardName: '' })
    },
    onError: (error: any) => {
      alert(error?.message || 'Ошибка добавления карты')
    }
  })

  const deleteCardMutation = useMutation({
    mutationFn: (cardId: number) => apiClient.delete(`/api/loyalty-cards/${cardId}`),
    onSuccess: () => {
      alert('✅ Карта удалена!')
      queryClient.invalidateQueries(['loyalty-cards'])
    }
  })

  const handleAddCard = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.cardNumber.trim()) {
      alert('Укажите номер карты')
      return
    }

    addCardMutation.mutate({
      cardType: formData.cardType,
      cardNumber: formData.cardNumber.trim(),
      cardName: formData.cardName.trim() || undefined,
      barcodeType: 'EAN13'
    })
  }

  const loyaltyCards = cardsData?.cards || []

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 overflow-y-auto">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6 my-8"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">💳 Карты лояльности</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Список карт */}
        <div className="space-y-3 mb-4">
          {loyaltyCards.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Gift className="h-12 w-12 mx-auto mb-2 text-gray-300" />
              <p>У вас пока нет карт лояльности</p>
            </div>
          ) : (
            loyaltyCards.map((card: any) => (
              <Card key={card.id}>
                <CardContent className="p-3 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="text-2xl">
                      {getCardIcon(card.cardType)}
                    </div>
                    <div>
                      <p className="font-medium text-sm">{card.cardName || getCardTypeName(card.cardType)}</p>
                      <p className="text-xs text-gray-500">{card.maskedNumber}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      if (confirm('Удалить эту карту?')) {
                        deleteCardMutation.mutate(card.id)
                      }
                    }}
                    className="text-red-500 hover:text-red-700 text-xs"
                  >
                    Удалить
                  </button>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Форма добавления */}
        {!showAddForm ? (
          <Button
            onClick={() => setShowAddForm(true)}
            className="w-full border-dashed"
            variant="outline"
          >
            <Plus className="mr-2 h-4 w-4" />
            Добавить карту
          </Button>
        ) : (
          <form onSubmit={handleAddCard} className="space-y-3 border-t pt-4">
            <div>
              <Label>Тип карты</Label>
              <select
                value={formData.cardType}
                onChange={(e) => setFormData({ ...formData, cardType: e.target.value })}
                className="w-full rounded-lg border px-3 py-2 text-sm"
              >
                <option value="MAGNIT">🛒 Магнит</option>
                <option value="PYATEROCHKA">🍎 Пятёрочка</option>
                <option value="LENTA">🏪 Лента</option>
                <option value="AUCHAN">🛍️ Ашан</option>
                <option value="LETUAL">💄 Летуаль</option>
                <option value="GOLDEN_APPLE">💎 Золотое Яблоко</option>
                <option value="OTHER">💳 Другая</option>
              </select>
            </div>

            <div>
              <Label>Номер карты</Label>
              <Input
                type="text"
                placeholder="1234567890123"
                value={formData.cardNumber}
                onChange={(e) => setFormData({ ...formData, cardNumber: e.target.value })}
              />
            </div>

            <div>
              <Label>Название (опционально)</Label>
              <Input
                type="text"
                placeholder="Моя карта Магнит"
                value={formData.cardName}
                onChange={(e) => setFormData({ ...formData, cardName: e.target.value })}
              />
            </div>

            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowAddForm(false)}
                className="flex-1"
                size="sm"
              >
                Отмена
              </Button>
              <Button
                type="submit"
                disabled={addCardMutation.isPending}
                className="flex-1 bg-purple-600"
                size="sm"
              >
                {addCardMutation.isPending ? 'Добавление...' : 'Добавить'}
              </Button>
            </div>
          </form>
        )}
      </motion.div>
    </div>
  )
}

// Модалка установки приоритетов
function SetPriorityModal({ 
  accounts, 
  onClose, 
  onSuccess 
}: { 
  accounts: any[], 
  onClose: () => void, 
  onSuccess: () => void 
}) {
  const [priorities, setPriorities] = useState<Record<number, number>>(
    accounts.reduce((acc, account, idx) => ({
      ...acc,
      [account.id]: idx + 1
    }), {})
  )

  const saveMutation = useMutation({
    mutationFn: async () => {
      const promises = Object.entries(priorities).map(([accountId, priority]) =>
        apiClient.put(`/api/accounts/${accountId}/priority?priority=${priority}`)
      )
      return Promise.all(promises)
    },
    onSuccess: () => {
      alert('✅ Приоритеты обновлены!')
      onSuccess()
    },
    onError: (error: any) => {
      alert(error?.message || 'Ошибка сохранения приоритетов')
    }
  })

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md rounded-2xl bg-white p-6 max-h-[80vh] overflow-y-auto"
      >
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-xl font-bold text-gray-900">Приоритет списания</h3>
          <button onClick={onClose} className="rounded-full p-1 hover:bg-gray-100">
            <X className="h-5 w-5" />
          </button>
        </div>

        <p className="mb-4 text-sm text-gray-600">
          Установите порядок списания при автоплатежах. 1 = первым списывается.
        </p>

        <div className="space-y-3 mb-4">
          {accounts.map((account) => (
            <Card key={`priority-${account.id || account.accountId}-${account.clientId}`}>
              <CardContent className="p-3">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <p className="font-medium text-sm">{account.accountName}</p>
                    <p className="text-xs text-gray-500">{account.clientName}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min={1}
                      max={10}
                      value={priorities[account.id || 0] || 1}
                      onChange={(e) => setPriorities({
                        ...priorities,
                        [account.id || 0]: parseInt(e.target.value) || 1
                      })}
                      className="w-16 rounded border border-gray-300 px-2 py-1 text-center text-sm"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="flex gap-3">
          <Button type="button" variant="outline" onClick={onClose} className="flex-1">
            Отмена
          </Button>
          <Button
            onClick={() => saveMutation.mutate()}
            disabled={saveMutation.isPending}
            className="flex-1 bg-purple-600 hover:bg-purple-700"
          >
            {saveMutation.isPending ? 'Сохранение...' : 'Сохранить'}
          </Button>
        </div>
      </motion.div>
    </div>
  )
}

// Хелперы для карт лояльности
function getCardIcon(type: string): string {
  const icons: Record<string, string> = {
    MAGNIT: '🛒',
    PYATEROCHKA: '🍎',
    LENTA: '🏪',
    AUCHAN: '🛍️',
    LETUAL: '💄',
    GOLDEN_APPLE: '💎',
    RIVEGAUCHE: '🎨',
    AZBUKA_VKUSA: '🥗',
    OTHER: '💳'
  }
  return icons[type] || '💳'
}

function getCardTypeName(type: string): string {
  const names: Record<string, string> = {
    MAGNIT: 'Магнит',
    PYATEROCHKA: 'Пятёрочка',
    LENTA: 'Лента',
    AUCHAN: 'Ашан',
    LETUAL: 'Летуаль',
    GOLDEN_APPLE: 'Золотое Яблоко',
    RIVEGAUCHE: 'Рив Гош',
    AZBUKA_VKUSA: 'Азбука Вкуса',
    OTHER: 'Другая карта'
  }
  return names[type] || type
}

// Импорт useQuery
import { useQuery } from '@tanstack/react-query'

