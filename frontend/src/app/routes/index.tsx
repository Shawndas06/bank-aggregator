import { createBrowserRouter, Navigate } from 'react-router-dom'
import { HomePage } from '@pages/home'
import { SignInPage } from '@pages/sign-in'
import { SignUpPage } from '@pages/sign-up'
import { VerifyEmailPage } from '@pages/verify-email'
import { DashboardPage } from '@pages/dashboard'
import { AccountsPage } from '@pages/accounts'
import { AccountDetailPage } from '@pages/account-detail'
import { GroupsPage } from '@pages/groups'
import { GroupDetailPage } from '@pages/group-detail'
import { GroupTransactionsPage } from '@pages/group-transactions'
import { ProfilePage } from '@pages/profile'
import { PremiumPage } from '@pages/premium'
import { ROUTES } from '@shared/config'

export const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <HomePage />,
  },
  {
    path: ROUTES.SIGN_IN,
    element: <SignInPage />,
  },
  {
    path: ROUTES.SIGN_UP,
    element: <SignUpPage />,
  },
  {
    path: ROUTES.VERIFY_EMAIL,
    element: <VerifyEmailPage />,
  },
  {
    path: ROUTES.DASHBOARD,
    element: <DashboardPage />,
    // TODO: Add ProtectedRoute wrapper in future
  },
  {
    path: ROUTES.ACCOUNTS,
    element: <AccountsPage />,
  },
  {
    path: '/accounts/:id',
    element: <AccountDetailPage />,
  },
  {
    path: ROUTES.GROUPS,
    element: <GroupsPage />,
  },
  {
    path: `${ROUTES.GROUPS}/:id`,
    element: <GroupDetailPage />,
  },
  {
    path: `${ROUTES.GROUPS}/:id/transactions`,
    element: <GroupTransactionsPage />,
  },
  {
    path: ROUTES.PROFILE,
    element: <ProfilePage />,
  },
  {
    path: ROUTES.PREMIUM,
    element: <PremiumPage />,
  },
  {
    path: '*',
    element: <Navigate to={ROUTES.HOME} replace />,
  },
])
