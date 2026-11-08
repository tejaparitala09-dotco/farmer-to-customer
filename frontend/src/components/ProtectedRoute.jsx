import { Navigate } from 'react-router-dom';

export default function ProtectedRoute({ user, role, children }) {
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (role && user.role !== role) {
    return <Navigate to={user.role === 'farmer' ? '/dashboard' : '/products'} replace />;
  }
  return children;
}
