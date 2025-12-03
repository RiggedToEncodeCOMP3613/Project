import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft } from 'lucide-react';

interface MakeRequestProps {
  onNavigate: (screen: Screen) => void;
}

export function MakeRequest({ onNavigate }: MakeRequestProps) {
  return (
    <WireframeContainer title="Make Request">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('student-main')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Main Menu
        </button>

        <div>
          <h3 className="text-gray-800 mb-6">Submit Service Hours Request</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-gray-600">Service</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter service</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block mb-2 text-gray-600">Date</label>
                <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                  <span className="text-gray-400">DD/MM/YYYY</span>
                </div>
              </div>
              <div>
                <label className="block mb-2 text-gray-600">Hours</label>
                <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                  <span className="text-gray-400">0.0</span>
                </div>
              </div>
            </div>



            <div>
              <label className="block mb-2 text-gray-600">Student ID</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter Student ID</span>
              </div>
            </div>

            <div>
              <label className="block mb-2 text-gray-600">Supervisor ID</label>
              <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                <span className="text-gray-400">Enter Supervisor ID</span>
              </div>
            </div>

          </div>

          <div className="flex gap-4 mt-8">
            <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
              Submit Request
            </button>
            <button 
              onClick={() => onNavigate('student-main')}
              className="flex-1 border-2 border-gray-800 bg-white text-gray-800 px-6 py-3 hover:bg-gray-100"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}