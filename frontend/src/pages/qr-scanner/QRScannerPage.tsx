import { useState } from 'react'
import { motion } from 'framer-motion'
import { MobileHeader } from '@widgets/header'
import { BottomNavigation } from '@widgets/bottom-navigation'
import { Card, CardContent, Button, Input, Label } from '@shared/ui'
import { QrCode, Scan, Send, Download, ArrowLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export function QRScannerPage() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<'scan' | 'generate'>('scan')
  const [amount, setAmount] = useState('')
  const [description, setDescription] = useState('')

  const handleGenerateQR = () => {
    if (!amount || parseFloat(amount) <= 0) {
      alert('❌ Укажите сумму для получения')
      return
    }
    alert(`✅ QR код сгенерирован!\n\nСумма: ${amount} ₽\nОписание: ${description || 'Без описания'}\n\nПокажите QR код плательщику для сканирования`)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 pb-20">
      <MobileHeader />

      <main className="container mx-auto px-4 py-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <button
            onClick={() => navigate(-1)}
            className="mb-4 flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-4 w-4" />
            Назад
          </button>

          <h2 className="mb-2 text-2xl font-bold text-gray-900">QR Платежи</h2>
          <p className="text-gray-600">Оплата и получение денег по QR коду</p>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.5 }}
          className="my-6"
        >
          <div className="flex gap-2 rounded-xl bg-white p-2 shadow-sm">
            <button
              onClick={() => setActiveTab('scan')}
              className={`flex-1 rounded-lg px-4 py-3 text-sm font-medium transition-all ${
                activeTab === 'scan'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <Scan className="mx-auto mb-1 h-5 w-5" />
              Сканировать
            </button>
            <button
              onClick={() => setActiveTab('generate')}
              className={`flex-1 rounded-lg px-4 py-3 text-sm font-medium transition-all ${
                activeTab === 'generate'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg'
                  : 'text-gray-600 hover:bg-gray-50'
              }`}
            >
              <QrCode className="mx-auto mb-1 h-5 w-5" />
              Получить
            </button>
          </div>
        </motion.div>

        {activeTab === 'scan' ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <Card>
              <CardContent className="p-8">
                <div className="text-center">
                  <div className="mx-auto mb-6 flex h-64 w-64 items-center justify-center rounded-2xl border-4 border-dashed border-purple-300 bg-purple-50">
                    <Scan className="h-24 w-24 text-purple-400" />
                  </div>
                  <h3 className="mb-2 text-lg font-semibold text-gray-900">
                    Отсканируйте QR код
                  </h3>
                  <p className="mb-6 text-sm text-gray-600">
                    Наведите камеру на QR код для оплаты
                  </p>
                  <Button
                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600"
                    onClick={() => alert('📸 Камера откроется в следующей версии!\n\n✨ Функция в разработке:\n• Сканирование QR кодов\n• Моментальная оплата\n• История QR платежей')}
                  >
                    <Scan className="mr-2 h-4 w-4" />
                    Открыть камеру
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.5 }}
          >
            <Card>
              <CardContent className="p-6">
                <h3 className="mb-4 text-lg font-semibold text-gray-900">
                  Создать QR код для получения денег
                </h3>
                <div className="space-y-4">
                  <div>
                    <Label>Сумма для получения (₽)</Label>
                    <Input
                      type="number"
                      placeholder="1000"
                      value={amount}
                      onChange={(e) => setAmount(e.target.value)}
                    />
                  </div>
                  <div>
                    <Label>Описание (необязательно)</Label>
                    <Input
                      type="text"
                      placeholder="За что платеж"
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                    />
                  </div>

                  {amount && parseFloat(amount) > 0 && (
                    <div className="mt-6 rounded-xl border-2 border-purple-200 bg-purple-50 p-6">
                      <div className="mx-auto mb-4 flex h-48 w-48 items-center justify-center rounded-xl bg-white">
                        <QrCode className="h-32 w-32 text-purple-600" />
                      </div>
                      <div className="text-center">
                        <p className="mb-1 text-2xl font-bold text-purple-600">
                          {amount} ₽
                        </p>
                        <p className="text-sm text-gray-600">{description || 'Без описания'}</p>
                      </div>
                    </div>
                  )}

                  <div className="flex gap-3 pt-2">
                    <Button
                      variant="outline"
                      onClick={() => navigate(-1)}
                      className="flex-1"
                    >
                      Отмена
                    </Button>
                    <Button
                      onClick={handleGenerateQR}
                      className="flex-1 bg-gradient-to-r from-purple-600 to-blue-600"
                    >
                      <QrCode className="mr-2 h-4 w-4" />
                      Сгенерировать
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Инструкции */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="mt-6"
        >
          <Card className="bg-gradient-to-r from-blue-50 to-purple-50">
            <CardContent className="p-4">
              <h4 className="mb-2 font-semibold text-gray-900">💡 Как это работает?</h4>
              <ul className="space-y-1 text-sm text-gray-700">
                <li>• <strong>Сканировать:</strong> Оплачивайте по QR коду в магазинах</li>
                <li>• <strong>Получить:</strong> Создайте QR для получения денег от друзей</li>
                <li>• <strong>Безопасно:</strong> Все платежи проходят через защищенное соединение</li>
              </ul>
            </CardContent>
          </Card>
        </motion.div>
      </main>

      <BottomNavigation />
    </div>
  )
}

