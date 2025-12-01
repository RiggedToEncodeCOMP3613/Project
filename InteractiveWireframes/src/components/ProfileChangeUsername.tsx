import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft } from 'lucide-react';

interface ChangeUsernameProps {
  onNavigate: (screen: Screen) => void;
  userType: 'student' | 'staff';
}

export function ChangeUsername({ onNavigate, userType = 'student' }: ChangeUsernameProps) {
  const backScreen = userType === 'staff' ? 'staff-profile' : 'student-profile';
  const title = userType === 'staff'
    ? 'Profile Screen > Change Username'
    : 'Profile Screen > Change Username';

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
          <h3 className="text-gray-800 mb-6">Change Username</h3>

          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-gray-600">Current Username</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-gray-100">
                <span className="text-gray-600">{userType === 'staff' ? 'staffmember' : 'student'}</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">New Username</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter new username</span>
              </div>
              <p className="text-gray-600 mt-1">Username must be 3-20 characters long</p>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">Confirm Password</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter your password to confirm</span>
              </div>
            </div>
          </div>

          <div className="flex gap-4 mt-8">
            <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
              Change Username
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
              <strong>Note:</strong> Changing your username will affect how you appear to other users.
            </p>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}