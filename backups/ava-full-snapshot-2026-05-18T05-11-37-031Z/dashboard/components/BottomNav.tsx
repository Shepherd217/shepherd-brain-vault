"use client";

import { ClipboardList, BarChart3, Users, Plus } from "lucide-react";

interface BottomNavProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
  onCreateTask: () => void;
}

export function BottomNav({ activeTab, onTabChange, onCreateTask }: BottomNavProps) {
  const tabs = [
    { id: "board", label: "Board", icon: ClipboardList },
    { id: "activity", label: "Activity", icon: BarChart3 },
    { id: "team", label: "Team", icon: Users },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-card border-t border-border">
      <div className="flex items-center justify-around h-16 pb-safe">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex flex-col items-center justify-center w-full h-full gap-0.5 transition-colors ${
                isActive
                  ? "text-primary"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <Icon className="h-5 w-5" />
              <span className="text-[10px] font-medium">{tab.label}</span>
              {isActive && (
                <div className="absolute bottom-0 w-12 h-0.5 bg-primary rounded-full" />
              )}
            </button>
          );
        })}
        <button
          onClick={onCreateTask}
          className="flex flex-col items-center justify-center w-full h-full gap-0.5 text-muted-foreground hover:text-foreground transition-colors"
        >
          <div className="flex items-center justify-center h-8 w-8 rounded-full bg-primary text-primary-foreground">
            <Plus className="h-5 w-5" />
          </div>
          <span className="text-[10px] font-medium">New</span>
        </button>
      </div>
    </nav>
  );
}