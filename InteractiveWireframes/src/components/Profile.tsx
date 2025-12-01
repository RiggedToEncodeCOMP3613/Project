import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, User, Mail, Lock } from 'lucide-react';

interface StudentProfileProps {
  onNavigate: (screen: Screen) => void;
  isStaff?: boolean;
}

export function StudentProfile({ onNavigate, isStaff = false }: StudentProfileProps) {
  const backScreen = isStaff ? 'staff-main' : 'student-main';
  const title = isStaff ? 'Profile Screen' : 'Profile Screen';

  return (
    <WireframeContainer title={title}>
      <div className="space-y-6">
        <button
          onClick={() => onNavigate(backScreen)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Main Menu
        </button>

        <div className="space-y-8">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 border-4 border-gray-800 flex items-center justify-center">
              <User className="w-12 h-12 text-gray-400" />
            </div>
            <div>
              <h3 className="text-gray-800">{isStaff ? 'Staff Name' : 'Student Name'}</h3>
              <p className="text-gray-600">{isStaff ? 'staff@sta.uwi.edu' : 'student@my.uwi.edu'}</p>
              <p className="text-gray-600">{isStaff ? 'Staff ID: 30016639' : 'Student ID: 816012534'}</p>
            </div>
          </div>

          <div className="border-t-2 border-gray-800 pt-6">
            <h4 className="text-gray-800 mb-4">Account Settings</h4>
            
            <div className="space-y-4">
              <button
                onClick={() => onNavigate(isStaff ? 'staff-update-username' : 'update-username')}
                className="w-full border-2 border-gray-800 p-4 hover:bg-gray-50 flex items-center justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 border-2 border-gray-800 flex items-center justify-center">
                    <User className="w-6 h-6" />
                  </div>
                  <div className="text-left">
                    <div className="text-gray-800">Change Username</div>
                    <div className="text-gray-600">Change your display name</div>
                  </div>
                </div>
                <div className="text-gray-400">→</div>
              </button>

              <button
                onClick={() => onNavigate(isStaff ? 'staff-update-email' : 'update-email')}
                className="w-full border-2 border-gray-800 p-4 hover:bg-gray-50 flex items-center justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 border-2 border-gray-800 flex items-center justify-center">
                    <Mail className="w-6 h-6" />
                  </div>
                  <div className="text-left">
                    <div className="text-gray-800">Change Email</div>
                    <div className="text-gray-600">Change your email address</div>
                  </div>
                </div>
                <div className="text-gray-400">→</div>
              </button>

              <button
                onClick={() => onNavigate(isStaff ? 'staff-update-password' : 'update-password')}
                className="w-full border-2 border-gray-800 p-4 hover:bg-gray-50 flex items-center justify-between"
              >
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 border-2 border-gray-800 flex items-center justify-center">
                    <Lock className="w-6 h-6" />
                  </div>
                  <div className="text-left">
                    <div className="text-gray-800">Change Password</div>
                    <div className="text-gray-600">Change your password</div>
                  </div>
                </div>
                <div className="text-gray-400">→</div>
              </button>
            </div>
          </div>

          {!isStaff && (
            <div className="border-t-2 border-gray-800 pt-6">
              <h4 className="text-gray-800 mb-4">Additional Information</h4>
              <div className="space-y-3">
                <div className="flex justify-between p-4 bg-gray-100 border-2 border-gray-800">
                  <span className="text-gray-600">Total Hours</span>
                  <span className="text-gray-800">42 hours</span>
                </div>
                <div className="flex justify-between p-4 bg-gray-100 border-2 border-gray-800">
                  <span className="text-gray-600">Milestones Earned</span>
                  <span className="text-gray-800">4</span>
                </div>
                <div className="flex justify-between p-4 bg-gray-100 border-2 border-gray-800">
                  <span className="text-gray-600">Accolades Earned</span>
                  <span className="text-gray-800">5</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </WireframeContainer>
  );
}