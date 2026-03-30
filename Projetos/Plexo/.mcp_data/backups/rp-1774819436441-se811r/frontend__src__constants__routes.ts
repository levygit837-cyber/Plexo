// Application route constants
// FEATURE: Navigation

export const ROUTES = {
  HOME: '/',
  AGENTS: '/agents',
  AGENT_DETAIL: '/agents/:id',
  AGENT_CREATE: '/agents/new',
  TASKS: '/tasks',
  TASK_DETAIL: '/tasks/:id',
  TASK_CREATE: '/tasks/new',
  MESSAGES: '/messages',
  SETTINGS: '/settings',
  PROFILE: '/profile',
  LOGIN: '/login',
  REGISTER: '/register',
  NOT_FOUND: '/404',
} as const;

export const buildRoute = {
  agentDetail: (id: string) => `/agents/${id}`,
  taskDetail: (id: string) => `/tasks/${id}`,
} as const;

export const ROUTE_TITLES: Record<string, string> = {
  [ROUTES.HOME]: 'Home',
  [ROUTES.AGENTS]: 'Agents',
  [ROUTES.AGENT_CREATE]: 'Create Agent',
  [ROUTES.TASKS]: 'Tasks',
  [ROUTES.TASK_CREATE]: 'Create Task',
  [ROUTES.MESSAGES]: 'Messages',
  [ROUTES.SETTINGS]: 'Settings',
  [ROUTES.PROFILE]: 'Profile',
  [ROUTES.LOGIN]: 'Login',
  [ROUTES.REGISTER]: 'Register',
};

export const PUBLIC_ROUTES = [ROUTES.LOGIN, ROUTES.REGISTER] as const;

export const PROTECTED_ROUTES = [
  ROUTES.HOME,
  ROUTES.AGENTS,
  ROUTES.TASKS,
  ROUTES.MESSAGES,
  ROUTES.SETTINGS,
  ROUTES.PROFILE,
] as const;
