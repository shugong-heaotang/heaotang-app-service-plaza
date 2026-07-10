import {
  createBusinessApiAdapter,
  defineBusinessRead,
  defineBusinessWrite,
  type BusinessApiExecutionOptions,
} from "../../infrastructure/businessApiAdapter";

/**
 * Compilable board-integration example. Copy its shape, then replace only the
 * service ID, endpoint paths and business request/response types.
 */
export type ExampleRecord = {
  id: number;
  title: string;
};

export type CreateExampleRecordInput = {
  title: string;
};

const api = createBusinessApiAdapter("example-service");

const listRecordsOperation = defineBusinessRead<void, { items: ExampleRecord[] }>({
  operationId: "list-records",
  path: () => "/api/v1/example/records",
});

const createRecordOperation = defineBusinessWrite<
  CreateExampleRecordInput,
  ExampleRecord
>({
  operationId: "create-record",
  method: "POST",
  path: () => "/api/v1/example/records",
  body: (input) => ({ title: input.title.trim() }),
});

export const exampleServiceApi = {
  async list(options?: BusinessApiExecutionOptions): Promise<ExampleRecord[]> {
    const result = await api.execute(listRecordsOperation, undefined, options);
    return result.items;
  },

  create(
    input: CreateExampleRecordInput,
    options?: BusinessApiExecutionOptions,
  ): Promise<ExampleRecord> {
    return api.execute(createRecordOperation, input, options);
  },
};
