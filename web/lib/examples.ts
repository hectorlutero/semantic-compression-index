export type ExampleId = "joao" | "secular" | "legal" | "scientific";

export const EXAMPLES: Record<
  ExampleId,
  { label: string; text: string }
> = {
  joao: {
    label: "João 1:1-5",
    text: `No princípio era o Verbo, e o Verbo estava com Deus, e o Verbo era Deus.
Ele estava no princípio com Deus.
Todas as coisas foram feitas por ele, e sem ele nada do que foi feito se fez.
Nele estava a vida, e a vida era a luz dos homens.
A luz resplandece nas trevas, e as trevas não prevaleceram contra ela.`,
  },
  secular: {
    label: "Secular",
    text: `Desde o começo existia a Visão. A Visão estava com o Fundador e a Visão era o próprio propósito da empresa. Tudo o que foi construído veio por meio dela. Sem ela nada do que existe teria sido feito. A Visão veio para o mercado, mas os próprios colaboradores não a receberam. Porém, a todos quantos a acolheram, ela deu o poder de se tornarem sócios. A Visão era a luz que iluminava o caminho, e as trevas da confusão não prevaleceram contra ela.`,
  },
  legal: {
    label: "Jurídico",
    text: `O contratante é obrigado a cumprir o prazo. É proibido ceder o contrato sem autorização. É permitido solicitar prorrogação salvo se houver justa causa. Se houver atraso, então aplica-se multa sob pena de rescisão.`,
  },
  scientific: {
    label: "Científico",
    text: `A hipótese inicial foi testada pelo método experimental. A evidência empírica observada sustenta a tese; portanto, conclui-se que o modelo é adequado. Sabe-se que o resultado é replicável.`,
  },
};
