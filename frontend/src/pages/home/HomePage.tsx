import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Button } from '@shared/ui'
import { ROUTES } from '@shared/config'

export function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 p-4 text-white">
      <div className="max-w-md text-center">
        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="mb-4 text-5xl font-bold"
        >
          Банк Агрегатор
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 0.9 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="mb-8 text-xl"
        >
          Управляй всеми своими счетами в одном месте
        </motion.p>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="flex flex-col gap-4"
        >
          <Button
            size="lg"
            variant="default"
            className="w-full bg-white text-purple-600 hover:bg-gray-100"
            onClick={() => navigate(ROUTES.SIGN_IN)}
          >
            Войти
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="w-full border-white/30 bg-white/10 text-white hover:bg-white/20"
            onClick={() => navigate(ROUTES.SIGN_UP)}
          >
            Регистрация
          </Button>
        </motion.div>
      </div>
    </div>
  )
}
