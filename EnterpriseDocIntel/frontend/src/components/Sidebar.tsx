"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
  { name: "Query Console", href: "/", icon: "🔍" },
  { name: "Document Library", href: "/library", icon: "📚" },
  { name: "Uploads", href: "/upload", icon: "⬆️" },
  { name: "Analytics", href: "/analytics", icon: "📊" },
  { name: "Settings", href: "/settings", icon: "⚙️" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex flex-col w-64 bg-slate-900 border-r border-slate-800 h-full p-4 text-slate-300">
      <div className="mb-8 px-2 flex flex-col gap-1">
        <h1 className="text-xl font-bold text-white tracking-tight leading-tight">
          Enterprise<br/>Doc Intel
        </h1>
        <span className="text-xs font-semibold text-emerald-400 tracking-wider uppercase">Platform v1.0</span>
      </div>

      <nav className="flex-1 space-y-1">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`${
                isActive
                  ? "bg-slate-800 text-white font-medium"
                  : "text-slate-400 hover:bg-slate-800/50 hover:text-slate-200"
              } group flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-colors`}
            >
              <span className="mr-3 text-lg">{item.icon}</span>
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto px-2 py-4 border-t border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold text-slate-300">
            AD
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-medium text-slate-200">Admin User</span>
            <span className="text-xs text-slate-500">Enterprise Tenant</span>
          </div>
        </div>
      </div>
    </div>
  );
}
