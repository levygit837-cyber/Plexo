// Application route constants | FEATURE: Navigation

export const ROUTES = {
    HOME: '/',
    LOGIN: '/login',
    REGISTER: '/register',
    AGENTS: '/agents',
    AGENT_DETAIL: '/agents/:id',
    TASKS: '/tasks',
    TASK_DETAIL: '/tasks/:id',
    CHAT: '/chat',
    SETTINGS: '/settings',
    PROFILE: '/profile',
    NOT_FOUND: '/404',
} as const;

export const buildRoute = (route: string, params: Record<string, string>) => {
    let builtRoute = route;
    Object.entries(params).forEach(([key, value]) => {
        builtRoute = builtRoute.replace(`:${key}`, value);
    });
    return builtRoute;
};

export const ROUTE_TITLES: Record<string, string> = {
    [ROUTES.HOME]: 'Home',
    [ROUTES.LOGIN]: 'Login',
    [ROUTES.REGISTER]: 'Register',
    [ROUTES.AGENTS]: 'Agentes',
    [ROUTES.TASKS]: 'Tarefas',
    [ROUTES.CHAT]: 'Chat',
    [ROUTES.SETTINGS]: 'Configurações',
    [ROUTES.PROFILE]: 'Perfil',
    [ROUTES.NOT_FOUND]: 'Página não encontrada',
};

export const PUBLIC_ROUTES = [ROUTES.LOGIN, ROUTES.REGISTER] as const;

export const PROTECTED_ROUTES = [
    ROUTES.AGENTS,
    ROUTES.TASKS,
    ROUTES.CHAT,
    ROUTES.SETTINGS,
    ROUTES.PROFILE,
] as const;
