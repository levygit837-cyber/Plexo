// Main route configuration with React Router
// FEATURE: Navigation
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import PrivateRoute from './PrivateRoute';
import { ROUTES } from '../constants/routes';

import Home from '../pages/Home';
import AgentsPage from '../pages/Agents';
import TasksPage from '../pages/Tasks';
import NotFound from '../pages/NotFound';

const AppRoutes: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to={ROUTES.HOME} replace />} />
          
          <Route
            path={ROUTES.HOME}
            element={
              <PrivateRoute>
                <Home />
              </PrivateRoute>
            }
          />
          
          <Route
            path={ROUTES.AGENTS}
            element={
              <PrivateRoute>
                <AgentsPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path={ROUTES.AGENT_DETAIL}
            element={
              <PrivateRoute>
                <AgentsPage />
              </PrivateRoute>
            }
          />
          
          <Route
            path={ROUTES.TASKS}
            element={
              <PrivateRoute>
                <TasksPage />
              </PrivateRoute>
            }
          />
          
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
