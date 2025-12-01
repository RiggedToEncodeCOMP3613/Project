import { ReactNode } from 'react';

interface WireframeContainerProps {
  title: string;
  children: ReactNode;
}

export function WireframeContainer({ title, children }: WireframeContainerProps) {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-5xl mx-auto px-6">
        <div className="bg-white border-4 border-gray-800 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]">
          <div className="border-b-4 border-gray-800 bg-gray-100 px-6 py-4">
            <h2 className="text-gray-800">{title}</h2>
          </div>
          <div className="p-8">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
