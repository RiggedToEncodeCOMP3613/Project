import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft } from 'lucide-react';

interface ChangeEmailProps {
  onNavigate: (screen: Screen) => void;
  userType: 'student' | 'staff';
}

export function ChangeEmail({ onNavigate, userType = 'student' }: ChangeEmailProps) {
  const backScreen = userType === 'staff' ? 'staff-profile' : 'student-profile';
  const title = userType === 'staff'
    ? 'Profile Screen > Change Email'
    : 'Profile Screen > Change Email';

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
          <h3 className="text-gray-800 mb-6">Change Email Address</h3>

          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-gray-600">Current Email</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-gray-100">
                <span className="text-gray-600">{userType === 'staff' ? 'staff@sta.uwi.edu' : 'student@my.uwi.edu'}</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">New Email Address</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter new email address</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">Confirm New Email</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Re-enter new email address</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">Current Password</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter your password to confirm</span>
              </div>
            </div>
          </div>

          <div className="flex gap-4 mt-8">
            <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
              Change Email
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
              <strong>Note:</strong> A verification email will be sent to your old email address. 
              You must verify your new email before the change takes effect.
            </p>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}