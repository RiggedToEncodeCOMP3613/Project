import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { Clock, Trophy, Target, User, LogOut, FileCheck } from 'lucide-react';

interface StaffMainMenuProps {
  onNavigate: (screen: Screen) => void;
}

export function StaffMainMenu({ onNavigate }: StaffMainMenuProps) {
  return (
    <WireframeContainer title="Staff Main Menu">
      <div className="space-y-6">
        <div className="flex justify-between items-center pb-4 border-b-2 border-gray-800">
          <div>
            <h3 className="text-gray-800">Welcome, Staff Name</h3>
            <p className="text-gray-600">Staff Dashboard</p>
          </div>
          <button 
            onClick={() => onNavigate('login')}
            className="flex items-center gap-2 px-4 py-2 border-2 border-gray-800 hover:bg-gray-100"
          >
            <LogOut className="w-4 h-4" />
            <span>Logout</span>
          </button>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <button
            onClick={() => onNavigate('staff-pending')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center relative">
              <FileCheck className="w-10 h-10" />
              <div className="absolute -top-2 -right-2 w-8 h-8 bg-red-500 border-2 border-gray-800 flex items-center justify-center text-white">
                4
              </div>
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">View Pending Requests</h4>
              <p className="text-gray-600">Review student submissions</p>
            </div>
          </button>

          <button
            onClick={() => onNavigate('log-hours')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center">
              <Clock className="w-10 h-10" />
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">Log Hours</h4>
              <p className="text-gray-600">Manually add student hours</p>
            </div>
          </button>

          <button
            onClick={() => onNavigate('milestones')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center">
              <Target className="w-10 h-10" />
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">Milestones</h4>
              <p className="text-gray-600">Manage milestones</p>
            </div>
          </button>

          <button
            onClick={() => onNavigate('accolades')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center">
              <Trophy className="w-10 h-10" />
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">Accolades</h4>
              <p className="text-gray-600">Manage & award accolades</p>
            </div>
          </button>

          <button
            onClick={() => onNavigate('staff-profile')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center">
              <User className="w-10 h-10" />
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">Profile</h4>
              <p className="text-gray-600">Manage your account</p>
            </div>
          </button>
        </div>

        <div className="border-2 border-gray-800 p-6 mt-8">
          <h4 className="text-gray-800 mb-4">System Overview</h4>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-gray-100">
              <div className="text-gray-800">4</div>
              <div className="text-gray-600">Active Students</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 border-2 border-yellow-300">
              <div className="text-gray-800">4</div>
              <div className="text-gray-600">Pending Requests</div>
            </div>
            <div className="text-center p-4 bg-gray-100">
              <div className="text-gray-800">6</div>
              <div className="text-gray-600">Active Accolades</div>
            </div>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}