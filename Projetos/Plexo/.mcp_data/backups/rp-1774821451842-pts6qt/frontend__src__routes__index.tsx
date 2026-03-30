// Main route configuration with React Router | FEATURE: Navigation
import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { Loading } from '../components/common/Loading';
import { PrivateRoute } from './PrivateRoute';

// Lazy load pages
const Home = lazy(() => import('../pages/Home').then(m => ({ default: m.Home })));
const Agents = lazy(() => import('../pages/Agents').then(m => ({ default: m.AgentsPage })));
const Tasks = lazy(() => import('../pages/Tasks').then(m => ({ default: m.TasksPage })));
const Chat = lazy(() => import('../pages/Chat').then(m => ({ default: m.ChatPage })));
const NotFound = lazy(() => import('../pages/NotFound').then(m => ({ default: m.NotFound })));

const AppRoutes: React.FC = () => {
    return (
        <Routes>
            {/* Public Routes */}
            <Route
                path="/"
                element={
                    <Layout>
                        <Suspense fallback={<Loading />}> 
                            <Home />
                        </Suspense>
                    </Layout>
                }
            />

            {/* Protected Routes */}
            <Route
                path="/chat"
                element={
                    <PrivateRoute>
                        <Suspense fallback={<Loading />}> 
                            <Chat />
                        </Suspense>
                    </PrivateRoute>
                }
            />
            <Route
                path="/agents"
                element={
                    <PrivateRoute>
                        <Layout>
                            <Suspense fallback={<Loading />}> 
                                <Agents />
                            </Suspense>
                        </Layout>
                    </PrivateRoute>
                }
            />
            <Route
                path="/tasks"
                element={
                    <PrivateRoute>
                        <Layout>
                            <Suspense fallback={<Loading />}> 
                                <Tasks />
                            </Suspense>
                        </Layout>
                    </PrivateRoute>
                }
            />

            {/* 404 */}
            <Route path="/404" element={<NotFound />} />
            <Route path="*" element={<Navigate to="/404" replace />} />
        </Routes>
    );
};

export { AppRoutes };
