// Footer component with copyright and links
// FEATURE: Layout

import React from 'react';
import { cn } from '../../../utils/helpers';

interface FooterProps {
  className?: string;
}

export const Footer: React.FC<FooterProps> = ({ className }) => {
  const currentYear = new Date().getFullYear();

  return (
    <footer
      className={cn(
        'border-t border-gray-200 dark:border-gray-700',
        'bg-white dark:bg-gray-800',
        className
      )}
    >
      <div className="px-4 py-6 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            © {currentYear} Plexo. All rights reserved.
          </p>
          <div className="flex gap-6">
            <a
              href="#"
              className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
            >
              Documentation
            </a>
            <a
              href="#"
              className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
            >
              Support
            </a>
            <a
              href="#"
              className="text-sm text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white"
            >
              Privacy
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};
