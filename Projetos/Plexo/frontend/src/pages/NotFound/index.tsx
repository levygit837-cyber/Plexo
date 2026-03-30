// 404 Not Found page component
// FEATURE: Navigation
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { ROUTES } from '../../constants/routes';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <div className="max-w-md w-full text-center">
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-gray-200 dark:text-gray-700">404</h1>
          <div className="mt-4">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
              Página não encontrada
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Desculpe, a página que você está procurando não existe ou foi movida.
            </p>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            variant="secondary"
            size="md"
            onClick={() => navigate(-1)}
          >
            <ArrowLeft size={20} className="mr-2" />
            Voltar
          </Button>
          <Link to={ROUTES.HOME}>
            <Button variant="primary" size="md">
              <Home size={20} className="mr-2" />
              Ir para Home
            </Button>
          </Link>
        </div>

        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
            Links úteis:
          </p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            <Link
              to={ROUTES.HOME}
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Dashboard
            </Link>
            <Link
              to={ROUTES.AGENTS}
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Agentes
            </Link>
            <Link
              to={ROUTES.TASKS}
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Tarefas
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
