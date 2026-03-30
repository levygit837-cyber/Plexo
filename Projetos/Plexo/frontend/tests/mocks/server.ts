// MSW server configuration for API mocking
// FEATURE: Testing
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
