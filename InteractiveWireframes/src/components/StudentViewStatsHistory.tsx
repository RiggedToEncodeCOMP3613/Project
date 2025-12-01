import { Screen } from '../App';
import { WireframeContainer } from './WireframeContainer';
import { ArrowLeft, Search } from 'lucide-react';

interface ViewStatsHistoryProps {
  onNavigate: (screen: Screen) => void;
}

export function ViewStatsHistory({ onNavigate }: ViewStatsHistoryProps) {
  const history = [
    {
      id: 1,
      service: 'Computer Lab',
      supervisor_id: 30016639,
      date_completed: '15/11/2025',
      hours: 16,
      status: 'Approved',
      date_responded: '17/11/2025'
    },
    {
      id: 2,
      service: 'Cleanup',
      supervisor_id: 30016639,
      date_completed: '10/11/2025',
      hours: 10,
      status: 'Approved',
      date_responded: '12/11/2025'
    },
    {
      id: 3,
      service: 'Community Service',
      supervisor_id: 30016639,
      date_completed: '05/11/2025',
      hours: 25,
      status: 'Denied',
      date_responded: '07/11/2025'
    },
    {
      id: 4,
      service: 'Community Service',
      supervisor_id: 30016639,
      date_completed: '28/10/2025',
      hours: 11,
      status: 'Approved',
      date_responded: '30/10/2025'
    },
    {
      id: 5,
      service: 'Classroom Setup',
      supervisor_id: 30016639,
      date_completed: '20/10/2025',
      hours: 5,
      status: 'Approved',
      date_responded: '22/10/2025'
    },
  ];

  return (
    <WireframeContainer title="View Request History">
      <div className="space-y-6">
        <button
          onClick={() => onNavigate('view-stats-menu')}
          className="flex items-center gap-2 text-gray-600 hover:text-gray-800"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Stats Menu
        </button>

        <div>
          <h3 className="text-gray-800 mb-6">Request History</h3>

          {/* Search and Filter */}
          <div className="flex gap-4 mb-6">
            <div className="flex-1 relative">
              <div className="border-2 border-gray-800 px-4 py-3 bg-white flex items-center gap-2">
                <Search className="w-5 h-5 text-gray-400" />
                <span className="text-gray-400">Search by activity name...</span>
              </div>
            </div>
            <div className="border-2 border-gray-800 px-4 py-3 bg-white flex items-center gap-2">
              <span className="text-gray-400">Filter: All</span>
              <span className="text-gray-400">▼</span>
            </div>
          </div>

          <div className="border-2 border-gray-800">
            {/* Table Header */}
            <div className="grid grid-cols-6 gap-4 p-4 bg-gray-800 text-white">
              <div>Service</div>
              <div>Date Completed</div>
              <div>Hours</div>
              <div>Status</div>
              <div>Supervisor ID</div>
              <div>Date Responded</div>
            </div>

            {/* Table Rows */}
            {history.map((request, index) => (
              <div
                key={request.id}
                className={`grid grid-cols-6 gap-4 p-4 border-t-2 border-gray-800 ${
                  index % 2 === 0 ? 'bg-white' : 'bg-gray-50'
                }`}
              >
                <div className="text-gray-800">{request.service}</div>
                <div className="text-gray-600">{request.date_completed}</div>
                <div className="text-gray-600">{request.hours}</div>
                <div>
                  <span className={`px-3 py-1 border border-gray-800 inline-block ${
                    request.status === 'Approved' ? 'bg-green-200' : 'bg-red-200'
                  }`}>
                    {request.status}
                  </span>
                </div>
                <div className="text-gray-600">{request.supervisor_id}</div>
                <div className="text-gray-600">{request.date_responded}</div>
              </div>
            ))}
          </div>

          <div className="mt-6 flex justify-between items-center">
            <div className="text-gray-600">Showing {history.length} of {history.length} requests</div>
            <div className="flex gap-2">
              <button className="px-4 py-2 border-2 border-gray-800 bg-white hover:bg-gray-100">
                Previous
              </button>
              <button className="px-4 py-2 border-2 border-gray-800 bg-gray-800 text-white">
                1
              </button>
              <button className="px-4 py-2 border-2 border-gray-800 bg-white hover:bg-gray-100">
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </WireframeContainer>
  );
}