// components/Sidebar.tsx
"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

const Sidebar = () => {
  const router = useRouter();
  const [active, setActive] = useState<string>("");

  const handleNavigation = (path: string) => {
    setActive(path);
    router.push(path);
  };

  const links = [
    { name: "Home", path: "/" },
    { name: "Input", path: "/input" },
    { name: "Results", path: "/result" },
  ];

  return (
    <div className="w-64 h-screen bg-[#72A603] text-red flex flex-col">
      <h2 className="text-center text-2xl font-bold py-4">Tree of Life</h2>
      <nav className="flex-1">
        <ul>
          {links.map((link) => (
            <li key={link.path} className="py-2 px-4">
              <button
                className={`w-full text-left p-2 rounded hover:bg-gray-700 ${
                  active === link.path ? "bg-gray-700" : ""
                }`}
                onClick={() => handleNavigation(link.path)}
              >
                {link.name}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;
