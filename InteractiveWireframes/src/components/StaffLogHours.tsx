import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Search } from 'lucide-react';

interface LogHoursProps {
  onNavigate: (screen: Screen) => void;
}

export function LogHours({ onNavigate }: LogHoursProps) {
  return (
    <WireframeContainer title="Log Hours (Manually log student hrs)">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('staff-main')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Main Menu
        </button>

        <div>
          <h3 className="text-gray-800 mb-6">Manually Log Student Hours</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block mb-2 text-gray-600">Search Student</label>
              <div className="relative">
                <div className="border-2 border-gray-800 px-4 py-3 bg-white flex items-center gap-2">
                  <Search className="w-5 h-5 text-gray-400" />
                  <span className="text-gray-400">Search by name or student ID...</span>
                </div>
              </div>
              {/* Student Search Results */}
              <div className="mt-2 border-2 border-gray-800 divide-y-2 divide-gray-800">
                {[
                  { id: 1, name: 'Shichellssichells Bidehschischore', studentId: '816012345' },
                  { id: 2, name: 'Ryan Gosling', studentId: '816012534' },
                  { id: 3, name: 'Itachi Uchiha', studentId: '816099999' },
                  { id: 4, name: 'Subaru Natsuki', studentId: '816010000' },
                ].map((student, index) => (
                  <button
                    key={index}
                    className="w-full p-3 hover:bg-gray-100 flex justify-between items-center text-left"
                  >
                    <div>
                      <div className="text-gray-800">{student.name}</div>
                      <div className="text-gray-600">ID: {student.studentId}</div>
                    </div>
                    <div className="text-gray-400">Select</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="border-t-2 border-gray-800 pt-6 mt-6">
              <div className="mb-4 p-3 bg-gray-100 border-2 border-gray-800">
                <div className="text-gray-800">Selected Student: <strong>Shichellssichells Bidehschischore</strong> (ID: 816012345)</div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block mb-2 text-gray-600">Service</label>
                  <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                    <span className="text-gray-400">Enter service name</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block mb-2 text-gray-600">Date Completed</label>
                    <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                      <span className="text-gray-400">MM/DD/YYYY</span>
                    </div>
                  </div>
                  <div>
                    <label className="block mb-2 text-gray-600">Hours</label>
                    <div className="border-2 border-gray-800 px-4 py-3 bg-white">
                      <span className="text-gray-400">0.0</span>
                    </div>
                  </div>
                </div>

              </div>
              <div className="flex gap-4 mt-8">
                <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700">
                  Log Hours
                </button>
                <button 
                  onClick={() => onNavigate('staff-main')}
                  className="flex-1 border-2 border-gray-800 bg-white text-gray-800 px-6 py-3 hover:bg-gray-100"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}