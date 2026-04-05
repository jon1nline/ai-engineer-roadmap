'use client'; // Indica que este componente tem interatividade (botões, inputs)

import { useRef, useState } from 'react';

type Mensagem = {
  role: 'user' | 'assistant';
  content: string;
};

const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

export default function Home() {
  // Estados: onde guardamos o que o usuário digita e a resposta da IA
  const [pergunta, setPergunta] = useState('');
  const [resposta, setResposta] = useState('');
  const [carregando, setCarregando] = useState(false);
  const [digitando, setDigitando] = useState(false);
  const [mensagens, setMensagens] = useState<Mensagem[]>([]);
  const requestIdRef = useRef(0);

  const animarDigitacao = async (texto: string, requestId: number) => {
    setResposta('');
    setDigitando(true);

    for (let i = 1; i <= texto.length; i++) {
      // Se uma nova pergunta foi enviada, interrompe a animação antiga.
      if (requestId !== requestIdRef.current) return;

      setResposta(texto.slice(0, i));

      const caractereAtual = texto[i - 1];
      const atraso = caractereAtual === ' ' ? 15 : 30;
      await new Promise((resolve) => setTimeout(resolve, atraso));
    }

    if (requestId === requestIdRef.current) {
      setDigitando(false);
    }
  };

  const enviarPergunta = async () => {
    const perguntaLimpa = pergunta.trim();
    if (!perguntaLimpa) return;

    const requestId = ++requestIdRef.current;
    const novaMensagemUsuario: Mensagem = { role: 'user', content: perguntaLimpa };
    const novoHistorico = [...mensagens, novaMensagemUsuario];

    setMensagens(novoHistorico);
    setPergunta('');
    setCarregando(true);
    setDigitando(false);
    setResposta('');

    try {
      const res = await fetch(`${apiBaseUrl}/perguntar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          pergunta: perguntaLimpa,
          historico: novoHistorico,
        }),
      });

      const data = await res.json();
      const respostaTexto = data.resposta || 'Sem resposta no momento.';
      await animarDigitacao(respostaTexto, requestId);

      if (requestId === requestIdRef.current) {
        setMensagens((prev) => [...prev, { role: 'assistant', content: respostaTexto }]);
      }
    } catch (error) {
      await animarDigitacao('Erro ao conectar com o backend.', requestId);
    } finally {
      if (requestId === requestIdRef.current) {
        setCarregando(false);
      }
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center p-24 bg-gray-900 text-white">
      <h1 className="text-4xl font-bold mb-8">Fogareu AI Chat</h1>
      
      <div className="w-full max-w-2xl bg-gray-800 p-6 rounded-lg shadow-xl">
        <textarea
          className="w-full p-4 bg-gray-700 rounded mb-4 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={4}
          placeholder="Digite sua dúvida sobre o projeto..."
          value={pergunta}
          onChange={(e) => setPergunta(e.target.value)}
        />
        
        <button
          onClick={enviarPergunta}
          disabled={carregando}
          className="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded font-bold transition-all disabled:bg-gray-600"
        >
          {carregando ? 'Pensando...' : 'Perguntar para a IA'}
        </button>

        {resposta && (
          <div className="mt-8 p-4 bg-gray-900 border-l-4 border-blue-500 rounded">
            <h2 className="text-blue-400 font-bold mb-2">Resposta:</h2>
            <p className="leading-relaxed whitespace-pre-wrap">
              {resposta}
              {digitando && <span className="animate-pulse">|</span>}
            </p>
          </div>
        )}
      </div>
    </main>
  );
}