/**
 * Replaces spaces with hyphens in a string
 * @param name The string to process
 * @returns The processed string with spaces replaced by hyphens
 */
export function replaceSpacesWithHyphens(name: string): string {
    return name.replace(/\s+/g, '-');
  }
  
  /**
   * Replaces hyphens with spaces in a string
   * @param name The string to process
   * @returns The processed string with hyphens replaced by spaces
   */
  export function replaceHyphensWithSpaces(name: string): string {
    return name.replace(/-+/g, ' ');
  }