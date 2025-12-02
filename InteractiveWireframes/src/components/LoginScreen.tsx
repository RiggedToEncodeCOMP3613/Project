import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';

interface LoginScreenProps {
  onNavigate: (screen: Screen) => void;
}

export function LoginScreen({ onNavigate }: LoginScreenProps) {
  return (
    <WireframeContainer title="Login Screen">
      <div className="max-w-md mx-auto space-y-6">
        <div className="text-center mb-8">
          <div className="w-24 h-24 border-4 border-gray-800 mx-auto mb-4 flex items-center justify-center">
            <span className="text-gray-400">LOGO</span>
          </div>
          <h3 className="text-gray-800">Service Hours Tracker</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block mb-2 text-gray-600">Username / Email</label>
            <div className="border-2 border-gray-800 px-4 py-3 bg-white">
              <span className="text-gray-400">Enter username or email</span>
            </div>
          </div>

          <div>
            <label className="block mb-2 text-gray-600">Password</label>
            <div className="border-2 border-gray-800 px-4 py-3 bg-white">
              <span className="text-gray-400">Enter password</span>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="w-5 h-5 border-2 border-gray-800"></div>
            <span className="text-gray-600">Remember me</span>
          </div>
        </div>

        <div className="space-y-3 pt-4">
          <button 
            onClick={() => onNavigate('student-main')}
            className="w-full border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700"
          >
            Login as Student
          </button>
          <button 
            onClick={() => onNavigate('staff-main')}
            className="w-full border-2 border-gray-800 bg-white text-gray-800 px-6 py-3 hover:bg-gray-100"
          >
            Login as Staff
          </button>
        </div>

        <div className="text-center pt-4">
          <a href="#" className="text-gray-600 underline">Forgot Password?</a>
        </div>
      </div>
    </WireframeContainer>
  );
}