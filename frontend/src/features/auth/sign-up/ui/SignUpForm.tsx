import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useNavigate } from 'react-router-dom'
import { UserPlus, Eye, EyeOff } from 'lucide-react'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  Button,
  Input,
} from '@shared/ui'
import { ROUTES } from '@shared/config'
import { signUpSchema, type SignUpFormData } from '../model/schema'
import { useSignUp } from '../api/signUp'
import { ApiError } from '@shared/api'

export function SignUpForm() {
  const navigate = useNavigate()
  const { mutate: signUp, isPending } = useSignUp()
  const [error, setError] = useState<string | null>(null)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  const form = useForm<SignUpFormData>({
    resolver: zodResolver(signUpSchema),
    defaultValues: {
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      name: '',
      birthDate: '',
    },
  })

  const onSubmit = (data: SignUpFormData) => {
    setError(null)
    // Remove confirmPassword before sending to backend
    const { confirmPassword: _, ...signUpData } = data
    signUp(signUpData, {
      onSuccess: () => {
        navigate(ROUTES.VERIFY_EMAIL, {
          state: { email: data.email },
        })
      },
      onError: (error) => {
        if (error instanceof ApiError) {
          setError(error.message)
        } else {
          setError('Произошла ошибка при регистрации. Попробуйте снова.')
        }
      },
    })
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        {error && (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
            {error}
          </div>
        )}

        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Имя</FormLabel>
              <FormControl>
                <Input placeholder="Иван Иванов" autoComplete="name" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input
                  type="email"
                  placeholder="ivan@example.com"
                  autoComplete="email"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="phone"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Номер телефона *</FormLabel>
              <FormControl>
                <Input
                  type="tel"
                  placeholder="+7 900 123 45 67"
                  autoComplete="tel"
                  {...field}
                />
              </FormControl>
              <FormMessage />
              <p className="text-xs text-gray-500">
                Для переводов по номеру телефона
              </p>
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Пароль</FormLabel>
              <FormControl>
                <div className="relative">
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    autoComplete="new-password"
                    className="pr-10"
                    {...field}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute top-1/2 right-3 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="confirmPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Подтвердите пароль</FormLabel>
              <FormControl>
                <div className="relative">
                  <Input
                    type={showConfirmPassword ? 'text' : 'password'}
                    placeholder="••••••••"
                    autoComplete="new-password"
                    className="pr-10"
                    {...field}
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute top-1/2 right-3 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showConfirmPassword ? (
                      <EyeOff className="h-5 w-5" />
                    ) : (
                      <Eye className="h-5 w-5" />
                    )}
                  </button>
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="birthDate"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Дата рождения</FormLabel>
              <FormControl>
                <Input type="date" max={new Date().toISOString().split('T')[0]} {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          className="w-full bg-blue-600 font-semibold text-white shadow-lg transition-all duration-200 hover:bg-blue-700 hover:shadow-xl"
          size="lg"
          disabled={isPending}
        >
          {isPending ? (
            <>
              <span className="animate-pulse">Регистрация...</span>
            </>
          ) : (
            <>
              <UserPlus className="mr-2 h-5 w-5" />
              Зарегистрироваться
            </>
          )}
        </Button>
      </form>
    </Form>
  )
}
