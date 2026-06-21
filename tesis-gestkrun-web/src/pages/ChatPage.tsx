import { useState, useRef, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { chatService } from '../features/chat/chatService';
import type { MessageDTO } from '../features/chat/chatService';
import { Send } from 'lucide-react';

export default function ChatPage() {
  const { id: projectId } = useParams<{ id: string }>();
  const [input, setInput] = useState('');
  const [allMessages, setAllMessages] = useState<MessageDTO[]>([]);
  const [cursor, setCursor] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const countRef = useRef(0);

  const loadMessages = async (cursorVal?: string) => {
    if (loading) return;
    setLoading(true);
    try {
      const data = await chatService.listMessages(projectId!, cursorVal);
      if (cursorVal) {
        setAllMessages(prev => [...data.data, ...prev]);
      } else {
        setAllMessages(data.data);
        setLoaded(true);
      }
      setCursor(data.next_cursor);
    } finally {
      setLoading(false);
    }
  };

  const sendMutation = useMutation({
    mutationFn: (contenido: string) => chatService.sendMessage(projectId!, contenido),
    onSuccess: (msg) => {
      setAllMessages(prev => [...prev, msg]);
      setInput('');
    },
  });

  const handleSend = () => {
    if (!input.trim() || sendMutation.isPending) return;
    sendMutation.mutate(input.trim());
  };

  useEffect(() => {
    if (allMessages.length > 0 && allMessages.length > countRef.current) {
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
    countRef.current = allMessages.length;
  }, [allMessages.length]);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Chat del Proyecto</h1>
        {!loaded && (
          <button onClick={() => loadMessages()} className="text-blue-600 text-sm hover:underline">
            Cargar mensajes
          </button>
        )}
      </div>

      <div className="bg-white rounded-lg shadow border border-gray-200 flex flex-col h-[600px]">
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {cursor && loaded && (
            <button
              onClick={() => loadMessages(cursor)}
              disabled={loading}
              className="w-full text-center text-sm text-blue-600 hover:text-blue-800 py-2 disabled:text-gray-400"
            >
              {loading ? 'Cargando...' : 'Cargar más mensajes'}
            </button>
          )}

          {allMessages.map(m => (
            <div key={m.id} className="flex gap-2">
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-xs font-medium text-blue-700 shrink-0">
                {(m.sender_nombre || m.sender_id).slice(0, 2).toUpperCase()}
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-0.5">
                  {m.sender_nombre || m.sender_id.slice(0, 8)} &middot; {new Date(m.fecha_envio).toLocaleTimeString()}
                </p>
                <p className="text-sm bg-gray-50 rounded-lg p-2">{m.contenido}</p>
              </div>
            </div>
          ))}
          {loading && <p className="text-gray-400 text-sm text-center">Cargando...</p>}
          {!loading && allMessages.length === 0 && loaded && (
            <p className="text-gray-400 text-sm text-center pt-10">No hay mensajes aún. ¡Envía el primero!</p>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="border-t p-3 flex gap-2">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            placeholder="Escribe un mensaje..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || sendMutation.isPending}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-300"
          >
            <Send size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
