import { Navigate } from 'react-router-dom';
export default function ProtectedRoute({ user, role, children }) { return !user ? <Navigate to="/login" replace /> : role && user.role !== role ? <Navigate to="/" replace /> : children; }
