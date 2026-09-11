import { Navigate, Route, Routes } from 'react-router-dom'
import AppShell from '../components/layout/AppShell'
import Login from '../pages/auth/Login'
import Register from '../pages/auth/Register'
import Dashboard from '../pages/Dashboard'
import ProductList from '../pages/products/ProductList'
import SalesHistory from '../pages/sales/SalesHistory'
import ChannelList from '../pages/channels/ChannelList'
import MarketResearch from '../pages/market/MarketResearch'
import MessengerConnect from '../pages/messenger/MessengerConnect'
import AgentChat from '../pages/agent/AgentChat'
import ReportList from '../pages/reports/ReportList'
import ModelProviderSettings from '../pages/settings/ModelProviderSettings'
import ProtectedRoute from './ProtectedRoute'

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<AppShell />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/products" element={<ProductList />} />
          <Route path="/sales" element={<SalesHistory />} />
          <Route path="/channels" element={<ChannelList />} />
          <Route path="/market" element={<MarketResearch />} />
          <Route path="/messenger" element={<MessengerConnect />} />
          <Route path="/agent" element={<AgentChat />} />
          <Route path="/reports" element={<ReportList />} />
          <Route path="/settings" element={<ModelProviderSettings />} />
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
