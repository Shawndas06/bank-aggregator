import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  ArrowLeft, Plus, CheckCircle, AlertTriangle,
  Users, Calendar, List, X
} from 'lucide-react'
import { format, parseISO } from 'date-fns'
import { ru } from 'date-fns/locale'
import {
  useObligations,
  useCreateObligation,
  useMarkObligationPaid,
  useDeleteObligation,
  useContributions,
  useCreateContribution,
  useConfirmContribution,
  useCancelContribution,
  useSharedResources,
  useSetSharedResource,
  useForecast,
} from '@entities/family-plan'
import { useGetGroupMembers } from '@entities/group'
import { useGetMe } from '@entities/user'

// ─── Форматирование ───────────────────────────────────────────────────────────

function fmt(rub: number) {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB', maximumFractionDigits: 0 }).format(rub)
}
function fmtDate(iso: string) {
  return format(parseISO(iso), 'd MMM yyyy', { locale: ru })
}

// ─── Компонент: статус обязательства ─────────────────────────────────────────

function ObligationStatusBadge({ status }: { status: string }) {
  const cfg: Record<string, { label: string; cls: string }> = {
    pending: { label: 'Ожидает', cls: 'bg-yellow-100 text-yellow-700' },
    paid: { label: 'Оплачено', cls: 'bg-green-100 text-green-700' },
    overdue: { label: 'Просрочено', cls: 'bg-red-100 text-red-700' },
    cancelled: { label: 'Отменено', cls: 'bg-gray-100 text-gray-500' },
  }
  const { label, cls } = cfg[status] ?? { label: status, cls: 'bg-gray-100 text-gray-500' }
  return <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${cls}`}>{label}</span>
}

function ContributionStatusBadge({ status }: { status: string }) {
  const cfg: Record<string, { label: string; cls: string }> = {
    proposed: { label: 'Предложен', cls: 'bg-blue-100 text-blue-700' },
    confirmed: { label: 'Подтверждён', cls: 'bg-green-100 text-green-700' },
    cancelled: { label: 'Отменён', cls: 'bg-gray-100 text-gray-500' },
  }
  const { label, cls } = cfg[status] ?? { label: status, cls: 'bg-gray-100 text-gray-500' }
  return <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${cls}`}>{label}</span>
}

// ─── TAB 1: Семейный план (обязательства + взносы) ───────────────────────────

function PlanTab({ groupId, currentUserId }: { groupId: number; currentUserId: number }) {
  const { data: obligations = [] } = useObligations(groupId)
  const { data: contributions = [] } = useContributions(groupId)
  const { data: members = [] } = useGetGroupMembers(groupId)

  const markPaid = useMarkObligationPaid(groupId)
  const deleteObligation = useDeleteObligation(groupId)
  const confirmContribution = useConfirmContribution(groupId)
  const cancelContribution = useCancelContribution(groupId)

  const [showObForm, setShowObForm] = useState(false)
  const [showContrForm, setShowContrForm] = useState(false)

  // Форма обязательства
  const [obName, setObName] = useState('')
  const [obAmount, setObAmount] = useState('')
  const [obDate, setObDate] = useState('')
  const [obResponsible, setObResponsible] = useState<number>(currentUserId)
  const createOb = useCreateObligation(groupId)

  // Форма взноса
  const [contrAmount, setContrAmount] = useState('')
  const [contrDate, setContrDate] = useState('')
  const [contrNote, setContrNote] = useState('')
  const createContr = useCreateContribution(groupId)

  const handleCreateObligation = () => {
    if (!obName || !obAmount || !obDate) return
    createOb.mutate(
      {
        name: obName,
        amount_rub: parseFloat(obAmount),
        due_date: new Date(obDate).toISOString(),
        responsible_user_id: obResponsible,
      },
      {
        onSuccess: () => {
          setObName(''); setObAmount(''); setObDate('')
          setShowObForm(false)
        },
      }
    )
  }

  const handleCreateContribution = () => {
    if (!contrAmount || !contrDate) return
    createContr.mutate(
      {
        amount_rub: parseFloat(contrAmount),
        expected_date: new Date(contrDate).toISOString(),
        note: contrNote || undefined,
      },
      {
        onSuccess: () => {
          setContrAmount(''); setContrDate(''); setContrNote('')
          setShowContrForm(false)
        },
      }
    )
  }

  return (
    <div className="space-y-6">
      {/* ── Обязательства ── */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Обязательства</h3>
          <button
            onClick={() => setShowObForm(true)}
            className="flex items-center gap-1 text-sm text-blue-600 font-medium"
          >
            <Plus className="w-4 h-4" /> Добавить
          </button>
        </div>

        <AnimatePresence>
          {showObForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-blue-50 rounded-xl p-4 mb-3 border border-blue-200 space-y-3"
            >
              <input
                className="w-full border rounded-lg px-3 py-2 text-sm"
                placeholder="Название (напр. Аренда квартиры)"
                value={obName}
                onChange={e => setObName(e.target.value)}
              />
              <input
                className="w-full border rounded-lg px-3 py-2 text-sm"
                type="number"
                placeholder="Сумма ₽"
                value={obAmount}
                onChange={e => setObAmount(e.target.value)}
              />
              <input
                className="w-full border rounded-lg px-3 py-2 text-sm"
                type="date"
                value={obDate}
                onChange={e => setObDate(e.target.value)}
              />
              <div>
                <label className="text-xs text-gray-600 block mb-1">Ответственный</label>
                <select
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  value={obResponsible}
                  onChange={e => setObResponsible(Number(e.target.value))}
                >
                  {members.map(m => (
                    <option key={m.userId} value={m.userId}>{m.name}</option>
                  ))}
                </select>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setShowObForm(false)}
                  className="flex-1 border rounded-lg py-2 text-sm text-gray-600"
                >
                  Отмена
                </button>
                <button
                  onClick={handleCreateObligation}
                  disabled={createOb.isPending}
                  className="flex-1 bg-blue-600 text-white rounded-lg py-2 text-sm font-medium"
                >
                  {createOb.isPending ? 'Сохраняем...' : 'Добавить'}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {obligations.length === 0 ? (
          <p className="text-gray-400 text-sm text-center py-4">Обязательств пока нет</p>
        ) : (
          <div className="space-y-2">
            {obligations.map(ob => (
              <motion.div
                key={ob.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900 truncate">{ob.name}</p>
                    <p className="text-xs text-gray-500 mt-0.5">
                      {fmtDate(ob.dueDate)} · {ob.responsibleUserName}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 ml-2 flex-shrink-0">
                    <span className="font-bold text-gray-900">{fmt(ob.amountRub)}</span>
                    <ObligationStatusBadge status={ob.status} />
                  </div>
                </div>
                {ob.status === 'pending' && (
                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={() => markPaid.mutate(ob.id)}
                      className="flex items-center gap-1 text-xs bg-green-50 text-green-700 border border-green-200 rounded-lg px-3 py-1.5 font-medium"
                    >
                      <CheckCircle className="w-3 h-3" /> Оплачено
                    </button>
                    <button
                      onClick={() => {
                        if (confirm(`Удалить "${ob.name}"?`)) deleteObligation.mutate(ob.id)
                      }}
                      className="flex items-center gap-1 text-xs text-red-500 border border-red-100 rounded-lg px-3 py-1.5"
                    >
                      <X className="w-3 h-3" /> Удалить
                    </button>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* ── Взносы ── */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Взносы участников</h3>
          <button
            onClick={() => setShowContrForm(true)}
            className="flex items-center gap-1 text-sm text-blue-600 font-medium"
          >
            <Plus className="w-4 h-4" /> Предложить
          </button>
        </div>

        <AnimatePresence>
          {showContrForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-green-50 rounded-xl p-4 mb-3 border border-green-200 space-y-3"
            >
              <p className="text-xs text-gray-500">
                Вы предлагаете внести деньги к определённой дате. Второй участник должен подтвердить.
              </p>
              <input
                className="w-full border rounded-lg px-3 py-2 text-sm"
                type="number"
                placeholder="Сумма взноса ₽"
                value={contrAmount}
                onChange={e => setContrAmount(e.target.value)}
              />
              <input
                className="w-full border rounded-lg px-3 py-2 text-sm"
                type="date"
                value={contrDate}
                onChange={e => setContrDate(e.target.value)}
              />
              <input
                className="w-full border rounded-lg px-3 py-2 text-sm"
                placeholder="Примечание (необязательно)"
                value={contrNote}
                onChange={e => setContrNote(e.target.value)}
              />
              <div className="flex gap-2">
                <button onClick={() => setShowContrForm(false)} className="flex-1 border rounded-lg py-2 text-sm text-gray-600">Отмена</button>
                <button
                  onClick={handleCreateContribution}
                  disabled={createContr.isPending}
                  className="flex-1 bg-green-600 text-white rounded-lg py-2 text-sm font-medium"
                >
                  {createContr.isPending ? 'Сохраняем...' : 'Предложить'}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {contributions.length === 0 ? (
          <p className="text-gray-400 text-sm text-center py-4">Взносов пока нет</p>
        ) : (
          <div className="space-y-2">
            {contributions.map(c => (
              <motion.div
                key={c.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-gray-900">{c.contributorName}</p>
                    <p className="text-xs text-gray-500 mt-0.5">
                      до {fmtDate(c.expectedDate)}
                      {c.note && ` · ${c.note}`}
                    </p>
                  </div>
                  <div className="flex items-center gap-2 ml-2 flex-shrink-0">
                    <span className="font-bold text-green-700">+{fmt(c.amountRub)}</span>
                    <ContributionStatusBadge status={c.status} />
                  </div>
                </div>
                {c.status === 'proposed' && c.contributorUserId !== currentUserId && (
                  <div className="flex gap-2 mt-3">
                    <button
                      onClick={() => confirmContribution.mutate(c.id)}
                      className="flex items-center gap-1 text-xs bg-green-50 text-green-700 border border-green-200 rounded-lg px-3 py-1.5 font-medium"
                    >
                      <CheckCircle className="w-3 h-3" /> Подтвердить
                    </button>
                    <button
                      onClick={() => cancelContribution.mutate(c.id)}
                      className="flex items-center gap-1 text-xs text-red-500 border border-red-100 rounded-lg px-3 py-1.5"
                    >
                      <X className="w-3 h-3" /> Отклонить
                    </button>
                  </div>
                )}
                {c.status === 'proposed' && c.contributorUserId === currentUserId && (
                  <div className="mt-2">
                    <button
                      onClick={() => cancelContribution.mutate(c.id)}
                      className="flex items-center gap-1 text-xs text-red-500 border border-red-100 rounded-lg px-3 py-1.5"
                    >
                      <X className="w-3 h-3" /> Отменить взнос
                    </button>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// ─── TAB 2: Календарь и прогноз ───────────────────────────────────────────────

function CalendarTab({ groupId }: { groupId: number }) {
  const [balance, setBalance] = useState('')
  const [reserve, setReserve] = useState('5000')
  const [showForecast, setShowForecast] = useState(false)
  const [committedBalance, setCommittedBalance] = useState(0)
  const [committedReserve, setCommittedReserve] = useState(5000)

  const { data: forecast, isLoading } = useForecast(
    groupId,
    committedBalance,
    committedReserve,
    30,
  )

  const handleCalculate = () => {
    const b = parseFloat(balance)
    const r = parseFloat(reserve)
    if (isNaN(b) || b < 0) return
    setCommittedBalance(b)
    setCommittedReserve(isNaN(r) ? 5000 : r)
    setShowForecast(true)
  }

  return (
    <div className="space-y-4">
      {/* Ввод баланса */}
      <div className="bg-white rounded-xl border border-gray-100 p-4 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">Параметры расчёта</h3>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-gray-500 block mb-1">
              Текущий баланс включённых счетов (₽)
            </label>
            <input
              className="w-full border rounded-lg px-3 py-2 text-sm"
              type="number"
              placeholder="Например: 55000"
              value={balance}
              onChange={e => setBalance(e.target.value)}
            />
          </div>
          <div>
            <label className="text-xs text-gray-500 block mb-1">
              Резерв на повседневные расходы (₽)
            </label>
            <input
              className="w-full border rounded-lg px-3 py-2 text-sm"
              type="number"
              placeholder="5000"
              value={reserve}
              onChange={e => setReserve(e.target.value)}
            />
          </div>
          <button
            onClick={handleCalculate}
            className="w-full bg-blue-600 text-white rounded-xl py-3 font-medium text-sm"
          >
            Рассчитать прогноз
          </button>
        </div>
      </div>

      {/* Результат прогноза */}
      {showForecast && (
        <>
          {isLoading ? (
            <div className="text-center py-8 text-gray-400">Считаем...</div>
          ) : forecast ? (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-4"
            >
              {/* Сводка */}
              <div className={`rounded-xl p-4 border ${forecast.first_risk_date ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                {forecast.first_risk_date ? (
                  <div className="flex items-start gap-3">
                    <AlertTriangle className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-red-800">Возможная нехватка средств</p>
                      <p className="text-sm text-red-700 mt-1">
                        {fmtDate(forecast.first_risk_date)} — плановый остаток опускается ниже резерва {fmt(forecast.reserve_rub)}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-start gap-3">
                    <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-semibold text-green-800">Денег должно хватить</p>
                      <p className="text-sm text-green-700 mt-1">
                        Плановый минимум за 30 дней: {fmt(forecast.min_balance_rub)}
                      </p>
                    </div>
                  </div>
                )}
              </div>

              {/* Цифры */}
              <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
                <div className="divide-y divide-gray-50">
                  {[
                    { label: 'Включённый баланс', value: fmt(forecast.included_balance_rub), color: 'text-gray-900' },
                    { label: 'Предстоящие обязательства', value: `−${fmt(forecast.total_obligations_rub)}`, color: 'text-red-600' },
                    { label: 'Подтверждённые взносы', value: `+${fmt(forecast.total_contributions_rub)}`, color: 'text-green-600' },
                    { label: 'Резерв (бытовые расходы)', value: fmt(forecast.reserve_rub), color: 'text-gray-500' },
                    { label: 'Мин. остаток за 30 дней', value: fmt(forecast.min_balance_rub), color: forecast.min_balance_rub < forecast.reserve_rub ? 'text-red-600 font-bold' : 'text-gray-900 font-bold' },
                  ].map(({ label, value, color }) => (
                    <div key={label} className="flex justify-between items-center px-4 py-3">
                      <span className="text-sm text-gray-600">{label}</span>
                      <span className={`text-sm ${color}`}>{value}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Посуточный список — только дни с событиями или риском */}
              <div>
                <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Ближайшие события</h3>
                <div className="space-y-2">
                  {forecast.days
                    .filter(d => d.events.length > 0 || d.is_risk)
                    .slice(0, 15)
                    .map(day => (
                      <div
                        key={day.date}
                        className={`rounded-xl p-3 border ${day.is_risk ? 'bg-red-50 border-red-200' : 'bg-white border-gray-100'}`}
                      >
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-xs font-medium text-gray-500">{fmtDate(day.date)}</span>
                          <span className={`text-sm font-bold ${day.planned_balance < 0 ? 'text-red-600' : day.is_risk ? 'text-orange-600' : 'text-gray-900'}`}>
                            {fmt(day.planned_balance)}
                          </span>
                        </div>
                        {day.events.map((ev, i) => (
                          <div key={i} className="flex justify-between text-xs text-gray-500 mt-0.5">
                            <span>
                              {ev.type === 'obligation' ? '📤 ' : '📥 '}
                              {ev.name ?? (ev.type === 'contribution' ? 'Взнос' : 'Расход')}
                            </span>
                            <span className={ev.amount_rub < 0 ? 'text-red-600' : 'text-green-600'}>
                              {ev.amount_rub > 0 ? '+' : ''}{fmt(ev.amount_rub)}
                            </span>
                          </div>
                        ))}
                      </div>
                    ))}
                </div>
              </div>

              {/* Disclaimer */}
              <p className="text-xs text-gray-400 bg-gray-50 rounded-xl p-3 leading-relaxed">
                ⚠️ {forecast.disclaimer}
              </p>
            </motion.div>
          ) : null}
        </>
      )}
    </div>
  )
}

// ─── TAB 3: Участники и ресурсы ───────────────────────────────────────────────

function MembersTab({ groupId, currentUserId }: { groupId: number; currentUserId: number }) {
  const { data: members = [] } = useGetGroupMembers(groupId)
  const { data: resources = [] } = useSharedResources(groupId)
  const setResource = useSetSharedResource(groupId)

  const [showResourceForm, setShowResourceForm] = useState(false)
  const [resourceType, setResourceType] = useState<'account' | 'fixed_amount'>('fixed_amount')
  const [fixedAmount, setFixedAmount] = useState('')

  const handleSetResource = () => {
    const payload =
      resourceType === 'fixed_amount'
        ? {
            resource_type: 'fixed_amount' as const,
            fixed_amount_kopecks: Math.round(parseFloat(fixedAmount) * 100),
          }
        : { resource_type: 'account' as const }

    setResource.mutate(payload, {
      onSuccess: () => {
        setShowResourceForm(false)
        setFixedAmount('')
      },
    })
  }

  return (
    <div className="space-y-6">
      {/* Участники */}
      <div>
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Участники</h3>
        <div className="space-y-2">
          {members.map(m => (
            <div key={m.userId} className="flex items-center gap-3 bg-white rounded-xl border border-gray-100 p-4 shadow-sm">
              <div className="w-9 h-9 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-sm">
                {m.name[0]}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 text-sm">{m.name}</p>
                <p className="text-xs text-gray-500">{m.role}</p>
              </div>
              {m.userId === currentUserId && (
                <span className="text-xs text-blue-600 bg-blue-50 rounded-full px-2 py-0.5">Вы</span>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Включённые ресурсы */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Включённые ресурсы</h3>
          <button
            onClick={() => setShowResourceForm(true)}
            className="flex items-center gap-1 text-sm text-blue-600 font-medium"
          >
            <Plus className="w-4 h-4" /> Настроить
          </button>
        </div>

        <div className="bg-blue-50 rounded-xl p-3 border border-blue-100 mb-3">
          <p className="text-xs text-blue-700">
            🔒 Приглашение в план не раскрывает ваши счета. Только явно включённый ресурс виден партнёру. Транзакции не передаются — только баланс.
          </p>
        </div>

        <AnimatePresence>
          {showResourceForm && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-gray-50 rounded-xl p-4 mb-3 border border-gray-200 space-y-3"
            >
              <div className="flex gap-2">
                <button
                  onClick={() => setResourceType('fixed_amount')}
                  className={`flex-1 text-sm rounded-lg py-2 border ${resourceType === 'fixed_amount' ? 'bg-blue-600 text-white border-blue-600' : 'text-gray-600 border-gray-200'}`}
                >
                  Фиксированный взнос
                </button>
                <button
                  onClick={() => setResourceType('account')}
                  className={`flex-1 text-sm rounded-lg py-2 border ${resourceType === 'account' ? 'bg-blue-600 text-white border-blue-600' : 'text-gray-600 border-gray-200'}`}
                >
                  Счёт (баланс)
                </button>
              </div>
              {resourceType === 'fixed_amount' && (
                <input
                  className="w-full border rounded-lg px-3 py-2 text-sm"
                  type="number"
                  placeholder="Фиксированная сумма взноса ₽"
                  value={fixedAmount}
                  onChange={e => setFixedAmount(e.target.value)}
                />
              )}
              {resourceType === 'account' && (
                <p className="text-xs text-gray-500">Партнёр увидит только текущий баланс, без истории операций.</p>
              )}
              <div className="flex gap-2">
                <button onClick={() => setShowResourceForm(false)} className="flex-1 border rounded-lg py-2 text-sm text-gray-600">Отмена</button>
                <button
                  onClick={handleSetResource}
                  disabled={setResource.isPending}
                  className="flex-1 bg-blue-600 text-white rounded-lg py-2 text-sm font-medium"
                >
                  {setResource.isPending ? 'Сохраняем...' : 'Включить'}
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {resources.length === 0 ? (
          <p className="text-gray-400 text-sm text-center py-4">Никто ещё не добавил ресурсы</p>
        ) : (
          <div className="space-y-2">
            {resources.map(r => (
              <div key={r.id} className="flex items-center justify-between bg-white rounded-xl border border-gray-100 p-4 shadow-sm">
                <div>
                  <p className="text-sm font-medium text-gray-900">{r.userName}</p>
                  <p className="text-xs text-gray-500">
                    {r.resourceType === 'fixed_amount'
                      ? `Фикс. взнос: ${fmt(r.fixedAmountRub ?? 0)}`
                      : 'Счёт (только баланс)'}
                  </p>
                </div>
                <CheckCircle className="w-5 h-5 text-green-500" />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

// ─── Главная страница ──────────────────────────────────────────────────────────

const TABS = [
  { id: 'plan', label: 'План', icon: List },
  { id: 'calendar', label: 'Календарь', icon: Calendar },
  { id: 'members', label: 'Участники', icon: Users },
] as const

type TabId = typeof TABS[number]['id']

export function FamilyPlanPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const groupId = Number(id)
  const { data: user } = useGetMe()
  const [activeTab, setActiveTab] = useState<TabId>('plan')

  if (!groupId) return null

  return (
    <div className="min-h-screen bg-gray-50 pb-8">
      {/* Header */}
      <div className="bg-white border-b border-gray-100 sticky top-0 z-10">
        <div className="flex items-center gap-3 px-4 py-3">
          <button onClick={() => navigate(`/groups/${groupId}`)} className="p-1 -ml-1">
            <ArrowLeft className="w-5 h-5 text-gray-700" />
          </button>
          <div>
            <h1 className="font-bold text-gray-900">Семейный план</h1>
            <p className="text-xs text-gray-500">Совместный бюджет и прогноз</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex border-t border-gray-100">
          {TABS.map(tab => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex-1 flex flex-col items-center gap-1 py-2 text-xs font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-500'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            )
          })}
        </div>
      </div>

      {/* Content */}
      <div className="px-4 py-4">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.18 }}
          >
            {activeTab === 'plan' && (
              <PlanTab groupId={groupId} currentUserId={user?.id ?? 0} />
            )}
            {activeTab === 'calendar' && (
              <CalendarTab groupId={groupId} />
            )}
            {activeTab === 'members' && (
              <MembersTab groupId={groupId} currentUserId={user?.id ?? 0} />
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}
