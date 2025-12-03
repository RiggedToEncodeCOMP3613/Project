import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft } from 'lucide-react';

interface ChangePasswordProps {
  onNavigate: (screen: Screen) => void;
  userType: 'student' | 'staff';
}

export function ChangePassword({ onNavigate, userType = 'student' }: ChangePasswordProps) {
  const backScreen = userType === 'staff' ? 'staff-profile' : 'student-profile';
  const title = userType === 'staff'
    ? 'Profile Screen > Change Password'
    : 'Profile Screen > Change Password';

  return (
    <WireframeContainer title={title}>
      <div className="space-y-6">
        <button
          onClick={() => onNavigate(backScreen)}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Profile
        </button>

        <div className="max-w-lg">
          <h3 className="text-gray-800 mb-6">Change Password</h3>

          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-gray-600">Current Password</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter current password</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">New Password</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter new password</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">Confirm New Password</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Re-enter new password</span>
              </div>
            </div>

            <div className="p-4 bg-gray-100 border-2 border-gray-800">
              <div className="text-gray-800 mb-2">Password Requirements:</div>
              <ul className="space-y-1 text-gray-600">
                <li className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-gray-800"></div>
                  At least 8 characters long
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-gray-800"></div>
                  Contains uppercase letter
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-gray-800"></div>
                  Contains lowercase letter
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-gray-800"></div>
                  Contains number
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-gray-800"></div>
                  Contains special character
                </li>
              </ul>
            </div>
          </div>

          <div className="flex gap-4 mt-8">
            <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
              Change Password
            </button>
            <button 
              onClick={() => onNavigate(backScreen)}
              className="flex-1 border-2 border-gray-800 bg-white text-gray-800 px-6 py-3 hover:bg-gray-100"
            >
              Cancel
            </button>
          </div>

          <div className="mt-6 p-4 bg-yellow-50 border-2 border-gray-800">
            <p className="text-gray-800">
              <strong>Security Tip:</strong> Use a strong, unique password that you don't use on other websites.
            </p>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}