// Sidebar.tsx
import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

interface NavItem {
  name: string;
  path: string;
  icon: JSX.Element;
}

const navItems: NavItem[] = [
  { name: 'Dashboard', path: '/', icon: <i className="fas fa-home" /> },
  { name: 'Credits', path: '/credits', icon: <i className="fas fa-leaf" /> },
  { name: 'Summary', path: '/summary', icon: <i className="fas fa-chart-bar" /> },
];

const Sidebar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`flex ${isOpen ? 'w-64' : 'w-20'} transition-width duration-300 h-screen bg-gray-800 text-white`}>
      <div className="flex flex-col justify-between w-full">
        {/* Top Section */}
        <div>
          <div className="flex items-center justify-between p-4">
            <h1 className={`text-xl font-bold ${!isOpen && 'hidden'}`}>My App</h1>
            <button onClick={toggleSidebar} className="text-white focus:outline-none">
              <i className={`fas ${isOpen ? 'fa-chevron-left' : 'fa-bars'}`} />
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="mt-6">
            {navItems.map((item) => (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-4 px-4 py-3 hover:bg-gray-700 transition ${
                    isActive ? 'bg-gray-700' : ''
                  }`
                }
              >
                {item.icon}
                <span className={`${!isOpen && 'hidden'}`}>{item.name}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Bottom Section */}
        <div className="p-4">
          <button className="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded">
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
