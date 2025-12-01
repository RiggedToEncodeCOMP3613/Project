import { Screen } from '../App';
import { ChevronDown } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

interface NavigationProps {
  currentScreen: Screen;
  onNavigate: (screen: Screen) => void;
}

export function Navigation({ currentScreen, onNavigate }: NavigationProps) {
  const [showDropdown, setShowDropdown] = useState(false);
  const currentItemRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (showDropdown && currentItemRef.current) {
      currentItemRef.current.scrollIntoView({ block: 'center', behavior: 'smooth' });
    }
  }, [showDropdown]);

  const screenLabels: Record<Screen, string> = {
    'login': 'Login Screen',
    'student-main': 'Student Main Menu',
    'make-request': 'Student Make Request',
    'view-stats-menu': 'Student View Stats Menu',
    'view-stats-accolades': 'Student View Stats All',
    'view-stats-pending': 'Student View Stats Pending',
    'view-stats-history': 'Student View Stats History',
    'student-profile': 'Student Profile',
    'update-username': 'Student Change Username',
    'update-email': 'Student Change Email',
    'update-password': 'Student Change Password',
    'staff-main': 'Staff Main Menu',
    'staff-pending': 'Staff View Pending Requests',
    'log-hours': 'Staff Log Hours',
    'milestones': 'Staff Milestones',
    'create-milestone': 'Staff Milestones Create',
    'accolades': 'Staff Accolades',
    'create-accolade': 'Staff Accolades Create',
    'award-accolade': 'Staff Accolades Award',
    'staff-profile': 'Staff Profile',
    'staff-update-username': 'Staff Change Username',
    'staff-update-email': 'Staff Change Email',
    'staff-update-password': 'Staff Change Password',
  };

  const screens: Screen[] = [
    'login',
    'student-main',
    'make-request',
    'view-stats-menu',
    'view-stats-accolades',
    'view-stats-pending',
    'view-stats-history',
    'student-profile',
    'update-username',
    'update-email',
    'update-password',
    'staff-main',
    'staff-pending',
    'log-hours',
    'milestones',
    'create-milestone',
    'accolades',
    'create-accolade',
    'award-accolade',
    'staff-profile',
    'staff-update-username',
    'staff-update-email',
    'staff-update-password',
  ];

  return (
    <div className="fixed top-0 left-0 right-0 bg-white border-b-2 border-gray-800 z-50">
      <div className="max-w-7xl mx-auto px-6 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-gray-400">QUICK NAVIGATION</h1>
          </div>
          <div className="relative">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="flex items-center gap-2 px-4 py-2 border-2 border-gray-800 bg-white hover:bg-gray-100"
            >
              <span className="text-gray-800">{screenLabels[currentScreen]}</span>
              <ChevronDown className="w-4 h-4" />
            </button>
            {showDropdown && (
              <div className="absolute right-0 mt-1 w-96 bg-white border-2 border-gray-800 max-h-96 overflow-y-auto">
                {screens.map((screen) => (
                  <button
                    key={screen}
                    ref={currentScreen === screen ? currentItemRef : null}
                    onClick={() => {
                      onNavigate(screen);
                      setShowDropdown(false);
                    }}
                    className={`block w-full text-left px-4 py-2 hover:bg-gray-100 border-b border-gray-200 ${
                      currentScreen === screen ? 'bg-gray-200' : ''
                    }`}
                  >
                    {screenLabels[screen]}
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}