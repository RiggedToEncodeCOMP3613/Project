import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Clock } from 'lucide-react';

interface ViewStatsPendingProps {
  onNavigate: (screen: Screen) => void;
}

export function ViewStatsPending({ onNavigate }: ViewStatsPendingProps) {
  const pendingRequests = [
    {
      id: 1,
      service: 'Classroom Setup',
      date_completed: '28/11/2025',
      hours: 4,
      status: 'Pending',
      supervisor_id: 30016639
    },
    {
      id: 2,
      service: 'Computer Lab',
      date_completed: '25/11/2025',
      hours: 3,
      status: 'Pending',
      supervisor_id: 30016639
    },
    {
      id: 3,
      service: 'Cleanup',
      date_completed: '20/11/2025',
      hours: 2.5,
      status: 'Pending',
      supervisor_id: 30016639
    },
  ];

  return (
    <WireframeContainer title="View Pending Requests">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('view-stats-menu')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Stats Menu
        </button>

        <div>
          <div className="flex items-center gap-3 mb-6">
            <Clock className="w-6 h-6" />
            <h3 className="text-gray-800">Pending Requests</h3>
            <div className="px-3 py-1 bg-yellow-200 border border-gray-800">
              <span className="text-gray-800">{pendingRequests.length} Pending</span>
            </div>
          </div>

          <div className="border-2 border-gray-800">
            {/* Table Header */}
            <div className="grid grid-cols-5 gap-4 p-4 bg-gray-800 text-white">
              <div>Service</div>
              <div>Date Completed</div>
              <div>Hours</div>
              <div>Status</div>
              <div>Supervisor ID</div>
            </div>

            {/* Table Rows */}
            {pendingRequests.map((request, index) => (
              <div
                key={request.id}
                className={`grid grid-cols-5 gap-4 p-4 border-t-2 border-gray-800 ${
                  index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                }`}
              >
                <div className="text-gray-800">{request.service}</div>
                <div className="text-gray-600">{request.date_completed}</div>
                <div className="text-gray-600">{request.hours}</div>
                <div>
                  <span className="px-3 py-1 bg-yellow-200 border border-gray-800 inline-block">
                    {request.status}
                  </span>
                </div>
                <div className="text-gray-600">{request.supervisor_id}</div>
              </div>
            ))}
          </div>

          {pendingRequests.length === 0 && (
            <div className="border-2 border-gray-800 p-12 text-center">
              <div className="text-gray-400">No pending requests</div>
            </div>
          )}

          <div className="mt-6 p-4 bg-gray-100 border-2 border-gray-800">
            <p className="text-gray-600">
              <strong>Note:</strong> Pending requests typically take 1 to 700 business days to review.
            </p>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}