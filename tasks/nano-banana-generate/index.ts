import type { Context } from "@oomol/types/oocana";

//#region generated meta
type Inputs = {
  prompt: string;
  num_images: number | null;
  output_format: "jpeg" | "png" | "webp" | null;
  aspect_ratio: "21:9" | "1:1" | "4:3" | "3:2" | "2:3" | "5:4" | "4:5" | "3:4" | "16:9" | "9:16" | null;
};
type Outputs = {
  session_id: string;
};
//#endregion

export default async function (
  params: Inputs,
  context: Context<Inputs, Outputs>
): Promise<Outputs> {
  const { prompt, num_images, output_format, aspect_ratio } = params;

  // Validate required parameter
  if (!prompt || prompt.trim().length === 0) {
    throw new Error("Prompt parameter is required and cannot be empty");
  }

  // Get OOMOL token from context
  const apiToken = await context.getOomolToken();

  // Build request body with optional parameters
  const requestBody: {
    prompt: string;
    numImages?: number;
    outputFormat?: "jpeg" | "png" | "webp";
    aspectRatio?: string;
  } = {
    prompt: prompt.trim(),
  };

  if (num_images !== null && num_images !== undefined) {
    requestBody.numImages = num_images;
  }

  if (output_format !== null && output_format !== undefined) {
    requestBody.outputFormat = output_format;
  }

  if (aspect_ratio !== null && aspect_ratio !== undefined) {
    requestBody.aspectRatio = aspect_ratio;
  }

  const apiUrl = "https://fusion-api.oomol.com/v1/fal-nano-banana/submit";

  try {
    context.reportProgress(10);

    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        Authorization: apiToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    context.reportProgress(50);

    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage = `API request failed with status ${response.status}`;
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage += `\nDetails: ${JSON.stringify(errorJson)}`;
      } catch {
        errorMessage += `\nResponse: ${errorText}`;
      }
      throw new Error(errorMessage);
    }

    const result = await response.json();

    context.reportProgress(90);

    // Validate response format
    if (!result.success) {
      throw new Error(
        `API request failed: ${JSON.stringify(result)}`
      );
    }

    if (!result.sessionID) {
      throw new Error(
        `API response missing sessionID: ${JSON.stringify(result)}`
      );
    }

    context.reportProgress(100);

    return {
      session_id: result.sessionID,
    };
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Nano Banana generate request failed: ${error.message}`);
    }
    throw new Error(
      `Nano Banana generate request failed: ${String(error)}`
    );
  }
}
