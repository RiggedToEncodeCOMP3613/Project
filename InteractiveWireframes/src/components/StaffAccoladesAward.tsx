import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Search, Trophy } from 'lucide-react';

interface AwardAccoladeProps {
  onNavigate: (screen: Screen) => void;
}

export function AwardAccolade({ onNavigate }: AwardAccoladeProps) {
  const students = [
    { id: 1, name: 'Shichellssichells Bidehschischore', studentId: '816012345', hours: 42, accolades: 5 },
    { id: 2, name: 'Ryan Gosling', studentId: '816012534', hours: 38, accolades: 2 },
    { id: 3, name: 'Itachi Uchiha', studentId: '816099999', hours: 55, accolades: 6 },
    { id: 4, name: 'Subaru Natsuki', studentId: '816010000', hours: 28, accolades: 3 },
  ];

  const availableAccolades = [
    'Leadership',
    'Rising Star',
    'Dedication',
    'Tax Fraud'
  ];

  return (
    <WireframeContainer title="Accolades > Award">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('accolades')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Accolades
        </button>

        <div>
          <h3 className="text-gray-800 mb-6">Award Accolade to Student</h3>

          <div className="space-y-6">
            {/* Step 1: Select Student */}
            <div className="border-4 border-gray-800 p-6">
              <h4 className="text-gray-800 mb-4">Step 1: Select Student</h4>
              
              <div className="mb-4">
                <div className="relative">
                  <div className="border-2 border-gray-800 px-4 py-3 bg-white flex items-center gap-2">
                    <Search className="w-5 h-5 text-gray-400" />
                    <span className="text-gray-400">Search by name or student ID...</span>
                  </div>
                </div>
              </div>

              <div className="border-2 border-gray-800">
                {/* Table Header */}
                <div className="grid grid-cols-5 gap-4 p-3 bg-gray-800 text-white">
                  <div>Student Name</div>
                  <div>Student ID</div>
                  <div>Total Hours</div>
                  <div>Current Accolades</div>
                  <div>Select</div>
                </div>

                {/* Table Rows */}
                {students.map((student, index) => (
                  <div 
                    key={student.id}
                    className={`grid grid-cols-5 gap-4 p-3 border-t-2 border-gray-800 ${
                      index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                    }`}
                  >
                    <div className="text-gray-800">{student.name}</div>
                    <div className="text-gray-600">{student.studentId}</div>
                    <div className="text-gray-600">{student.hours}</div>
                    <div className="text-gray-600">{student.accolades}</div>
                    <div>
                      <button className="px-3 py-1 border-2 border-gray-800 bg-white hover:bg-gray-100">
                        Select
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Step 2: Choose Accolade */}
            <div className="border-4 border-gray-800 p-6 bg-gray-50">
              <h4 className="text-gray-800 mb-4">Step 2: Choose Accolade</h4>
              
              <div className="mb-4 p-3 bg-white border-2 border-gray-800">
                <div className="text-gray-800">Selected Student: <strong>Ryan Gosling</strong> (ID: 816012534)</div>
              </div>

              <div>
                <label className="block mb-2 text-gray-600">Select Accolade to Award</label>
                <div className="border-2 border-gray-800 px-4 py-3 bg-white flex justify-between items-center">
                  <span className="text-gray-400">Choose an accolade...</span>
                  <span className="text-gray-400">▼</span>
                </div>
              </div>

              <div className="mt-4 grid grid-cols-2 gap-3">
                {availableAccolades.map((accolade, index) => (
                  <button
                    key={index}
                    className="border-2 border-gray-800 p-4 bg-white hover:bg-yellow-50 flex items-center gap-3"
                  >
                    <div className="w-12 h-12 border-2 border-gray-800 flex items-center justify-center bg-yellow-100">
                      <Trophy className="w-6 h-6" />
                    </div>
                    <div className="text-left">
                      <div className="text-gray-800">{accolade}</div>
                    </div>
                  </button>
                ))}
              </div>

               <div className="mt-6 p-4 bg-gray-100 border-2 border-gray-800">
                <p className="text-gray-800">
                  <strong>Note:</strong> Students cannot be awarded duplicate accolades.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <button className="flex-1 border-2 border-gray-800 bg-gray-800 text-white px-6 py-3 hover:bg-gray-700 flex items-center justify-center gap-2">
                <Trophy className="w-5 h-5" />
                Award Accolade
              </button>
              <button 
                onClick={() => onNavigate('accolades')}
                className="flex-1 border-2 border-gray-800 bg-white text-gray-800 px-6 py-3 hover:bg-gray-100"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}