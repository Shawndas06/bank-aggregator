import { AccountDetailPage } from '@pages/account-detail'
import { AccountsPage } from '@pages/accounts'
import { AnalyticsPage } from '@pages/analytics'
import { CashbackPage } from '@pages/cashback/CashbackPage'
import { DashboardPage } from '@pages/dashboard'
import { GroupDetailPage } from '@pages/group-detail'
import { GroupTransactionsPage } from '@pages/group-transactions'
import { GroupsPage } from '@pages/groups'
import { FamilyPlanPage } from '@pages/family-plan'
import { HomePage } from '@pages/home'
import { LoyaltyCardsPage } from '@pages/loyalty-cards'
import { PaymentsPage } from '@pages/payments'
import { PremiumPage } from '@pages/premium'
import { ProfilePage } from '@pages/profile'
import { QRScannerPage } from '@pages/qr-scanner'
import { ReferralsPage } from '@pages/referrals'
import { SignInPage } from '@pages/sign-in'
import { SignUpPage } from '@pages/sign-up'
import { TransactionsPage } from '@pages/transactions'
import { VerifyEmailPage } from '@pages/verify-email'
import { ROUTES } from '@shared/config'
import { createBrowserRouter, Navigate } from 'react-router-dom'

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
    path: `${ROUTES.GROUPS}/:id/plan`,
    element: <FamilyPlanPage />,
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
    path: '/analytics',
    element: <AnalyticsPage />,
  },
  {
    path: '/payments',
    element: <PaymentsPage />,
  },
  {
    path: '/loyalty-cards',
    element: <LoyaltyCardsPage />,
  },
  {
    path: '/qr-scanner',
    element: <QRScannerPage />,
  },
  {
    path: ROUTES.REFERRALS,
    element: <ReferralsPage />,
  },
  {
    path: ROUTES.CASHBACK,
    element: <CashbackPage />,
  },
  {
    path: '/transactions',
    element: <TransactionsPage />,
  },
  {
    path: '*',
    element: <Navigate to={ROUTES.HOME} replace />,
  },
])
