import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Check, X } from 'lucide-react';

interface StaffPendingRequestsProps {
  onNavigate: (screen: Screen) => void;
}

export function StaffPendingRequests({ onNavigate }: StaffPendingRequestsProps) {
  const pendingRequests = [
    {
      id: 1,
      student: 'Shichellssichells Bidehschischore',
      studentId: '816012345',
      activity: 'Beach Cleanup',
      date: '28/11/2025',
      hours: 4,
      submitted: '29/11/2025'
    },
    {
      id: 2,
      student: 'Ryan Gosling',
      studentId: '816012534',
      activity: 'Computer Lab',
      date: '25/11/2025',
      hours: 3,
      submitted: '26/11/2025'
    },
    {
      id: 3,
      student: 'Itachi Uchiha',
      studentId: '816099999',
      activity: 'Classroom Setup',
      date: '20/11/2025',
      hours: 2.5,
      submitted: '21/11/2025'
    },
    {
      id: 4,
      student: 'Subaru Natsuki',
      studentId: '816010000',
      activity: 'Community Service',
      date: '18/11/2025',
      hours: 5,
      submitted: '19/11/2025'
    },
  ];

  return (
    <WireframeContainer title="View Pending Requests Screen">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('staff-main')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Main Menu
        </button>

        <div>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <h3 className="text-gray-800">Pending Student Requests</h3>
              <div className="px-3 py-1 bg-yellow-200 border border-gray-800">
                <span className="text-gray-800">{pendingRequests.length} Pending</span>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="border-2 border-gray-800 px-4 py-2 bg-white flex items-center gap-2">
                <span className="text-gray-400">Sort by: Date</span>
                <span className="text-gray-400">▼</span>
              </div>
            </div>
          </div>

          <div className="border-2 border-gray-800">
            {/* Table Header */}
            <div className="grid grid-cols-6 gap-4 p-4 bg-gray-800 text-white">
              <div>Student</div>
              <div>Student ID</div>
              <div>Service</div>
              <div>Date Completed</div>
              <div>Hours</div>
              <div>Actions</div>
            </div>

            {/* Table Rows */}
            {pendingRequests.map((request, index) => (
              <div 
                key={request.id}
                className={`grid grid-cols-6 gap-4 p-4 border-t-2 border-gray-800 ${
                  index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                }`}
              >
                <div className="text-gray-800">{request.student}</div>
                <div className="text-gray-600">{request.studentId}</div>
                <div className="text-gray-800">{request.activity}</div>
                <div className="text-gray-600">{request.date}</div>
                <div className="text-gray-600">{request.hours}</div>
                <div className="flex gap-2">
                  <button className="p-2 border-2 border-gray-800 bg-green-200 hover:bg-green-300" title="Approve">
                    <Check className="w-4 h-4" />
                  </button>
                  <button className="p-2 border-2 border-gray-800 bg-red-200 hover:bg-red-300" title="Reject">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>

        </div>
      </div>
    </WireframeContainer>
  );
}