import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { FileText, BarChart3, User, LogOut } from 'lucide-react';

interface StudentMainMenuProps {
  onNavigate: (screen: Screen) => void;
}

export function StudentMainMenu({ onNavigate }: StudentMainMenuProps) {
  return (
    <WireframeContainer title="Student Main Menu">
      <div className="space-y-6">
        <div className="flex justify-between items-center pb-4 border-b-2 border-gray-800">
          <div>
            <h3 className="text-gray-800">Welcome, Student Name</h3>
            <p className="text-gray-600">Student Dashboard</p>
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
            onClick={() => onNavigate('make-request')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center">
              <FileText className="w-10 h-10" />
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">Make Request</h4>
              <p className="text-gray-600">Submit hours for approval</p>
            </div>
          </button>

          <button
            onClick={() => onNavigate('view-stats-menu')}
            className="border-4 border-gray-800 p-8 hover:bg-gray-50 flex flex-col items-center gap-4"
          >
            <div className="w-20 h-20 border-2 border-gray-800 flex items-center justify-center">
              <BarChart3 className="w-10 h-10" />
            </div>
            <div className="text-center">
              <h4 className="text-gray-800">View Detailed Stats</h4>
              <p className="text-gray-600">Check your progress</p>
            </div>
          </button>

          <button
            onClick={() => onNavigate('student-profile')}
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
          <h4 className="text-gray-800 mb-4">Quick Stats</h4>
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-100">
              <div className="text-gray-800">42</div>
              <div className="text-gray-600">Total Hours</div>
            </div>
            <div className="text-center p-4 bg-gray-100">
              <div className="text-gray-800">3</div>
              <div className="text-gray-600">Pending Requests</div>
            </div>
            <div className="text-center p-4 bg-gray-100">
              <div className="text-gray-800">4</div>
              <div className="text-gray-600">Milestones</div>
            </div>
            <div className="text-center p-4 bg-gray-100">
              <div className="text-gray-800">5</div>
              <div className="text-gray-600">Accolades</div>
            </div>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}