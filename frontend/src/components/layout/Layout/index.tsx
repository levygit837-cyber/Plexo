// Main layout component combining Header, Sidebar, and Footer
// FEATURE: Layout

import React, { useState, ReactNode } from 'react';
import { Header } from '../Header';
import { Sidebar } from '../Sidebar';
import { Footer } from '../Footer';
import { cn } from '../../../utils/helpers';

interface LayoutProps {
  children: ReactNode;
  showSidebar?: boolean;
  showFooter?: boolean;
  className?: string;
}

export const Layout: React.FC<LayoutProps> = ({
  children,
  showSidebar = true,
  showFooter = true,
  className,
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <Header onMenuClick={() => setSidebarOpen(true)} />
      
      <div className="flex flex-1 overflow-hidden">
        {showSidebar && (
          <Sidebar
            isOpen={sidebarOpen}
            onClose={() => setSidebarOpen(false)}
          />
        )}
        
        <main
          className={cn(
            'flex-1 overflow-y-auto',
            'px-4 py-6 sm:px-6 lg:px-8',
            className
          )}
        >
          {children}
        </main>
      </div>
      
      {showFooter && <Footer />}
    </div>
  );
};
