import { Identity } from "@semaphore-protocol/identity"
import { Group } from "@semaphore-protocol/group"
import { generateProof } from "@semaphore-protocol/proof"

/**
 * @param {string} externalNullifier - The scope or context (e.g., your analysis session ID)
 * @param {string} message - The signal/message being sent anonymously
 */
export async function createAnonymousProof(externalNullifier, message) {
  const identity = new Identity()
  
  const group = new Group([identity.commitment])

  const fullProof = await generateProof(
    identity, 
    group, 
    message, 
    externalNullifier, 
    20 
  )

  return fullProof
}