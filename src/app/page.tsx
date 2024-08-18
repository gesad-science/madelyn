"use client";

import type { NextPage } from 'next';
import styles from '/home/janaina-santos/uimadelyn/styles/Home.module.scss';
import { useEffect, useState } from 'react';

//A seguinte aplicação utiliza o local storage para armazenar as aplicações criadas, e permite adicionar, editar e deletar aplicações
//interface para adicionar novos valores nas variáveis title, description, user (criador)
interface ApplicationBox {
  id: number;
  title: string;
  description: string;
  user: {
    name: string;
  };
  handleDelete?: (id: number) => void;
  handleEdit?: (id: number) => void;
}


//Cria uma lista para as aplicações do tipo ApplicationBox
const Home: NextPage = () => {
  const [applications, setApplications] = useState<ApplicationBox[]>([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const storedApplications = localStorage.getItem('applications');
    if (storedApplications) {
      setApplications(JSON.parse(storedApplications));
    }
  }, []);


//Função para deletar uma nova caixa com os valores de nome da aplicação, nome do criador e descrição
const handleDelete = (id: number) => {
    const newApplications = applications.filter(application => application.id !== id);
    setApplications(newApplications);
    localStorage.setItem('applications', JSON.stringify(newApplications));
  };


//Função para adicionar uma nova caixa com os valores de nome da aplicação, nome do criador e descrição
const handleAdd = () => {
    const nomeAplicacao = prompt("Digite o nome da aplicação:");
    const nomeCriador = prompt("Digite o nome do criador:");
    const descricao = prompt("Digite a descrição:");

    if (nomeAplicacao && nomeCriador && descricao) {
      const novaAplicacao: ApplicationBox = {
        id: applications.length + 1,
        title: nomeAplicacao,
        description: descricao,
        user: {
          name: nomeCriador,
        },
      };
      
      const updatedApplications = [...applications, novaAplicacao];
      setApplications(updatedApplications);
      localStorage.setItem('applications', JSON.stringify(updatedApplications));
    }
  };


//Função para editar uma nova caixa com os valores de nome da aplicação, nome do criador e descrição
const handleEdit = (id: number) => {
    const applicationToEdit = applications.find(app => app.id === id);
    if (applicationToEdit) {
      const novoNomeAplicacao = prompt("Editar nome da aplicação:", applicationToEdit.title);
      const novoNomeCriador = prompt("Editar nome do criador:", applicationToEdit.user.name);
      const novaDescricao = prompt("Editar descrição:", applicationToEdit.description);

      if (novoNomeAplicacao && novoNomeCriador && novaDescricao) {
        const updatedApplications = applications.map(app => 
          app.id === id ? { ...app, title: novoNomeAplicacao, user: { name: novoNomeCriador }, description: novaDescricao } : app
        );
        setApplications(updatedApplications);
        localStorage.setItem('applications', JSON.stringify(updatedApplications));
      }
    }
  };


//função para filtrar as aplicações
const filteredApplications = applications.filter(application =>
    application.title.toLowerCase().includes(searchTerm.toLowerCase())
);


//Retorna o html da página
  return (
    <html>
      <body>
        <main className={styles.container}>
          <div className={styles.caixaapps}>

          <div className={styles.actionBar}>
          <h1>Ficha de Treinos</h1>
          <button className={styles.novo} onClick={handleAdd}>Novo Treino</button>
          </div>
            <input
              type="text"
              placeholder="Digite o titulo da busca..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />

            {filteredApplications.map((application) => (
                  <ApplicationBox
                    key={application.id}
                    handleDelete={handleDelete}
                    handleEdit={handleEdit}
                    id={application.id}
                    title={application.title}
                    description={application.description}
                    user={{ name: application.user.name }}
                  />
                ))}
        
          </div>
        </main>
      </body>
    </html>
  );
};

export default Home;

//Cria uma caixa para as aplicações do tipo ApplicationBox
const ApplicationBox = ({ id, title, description, user, handleDelete, handleEdit }: ApplicationBox) => {
  return (
    <div className={styles.divapps}>
      <div className={styles.boxedit}>
        <p className={styles.NomeApp}>{title}</p>
        <div>
          <button className={styles.editar} onClick={() => handleEdit?.(id)}>Editar</button>
          <button className={styles.excluir} onClick={() => handleDelete?.(id)}>Excluir</button>
        </div>
      </div>

      <div className={styles.DescricaoAPP}>
        <p className={styles.NomeCriador}>{user.name}</p>
        <p className={styles.DescricaooApp}>{description}</p>
      </div>
    </div>
  );
};
