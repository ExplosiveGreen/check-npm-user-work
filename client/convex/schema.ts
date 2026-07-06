import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
    events: defineTable({
        name: v.string(),
        date: v.string(),
        links: v.object({
            bugs: v.optional(v.string()),
            homepage: v.optional(v.string()),
            npm: v.string(),
            repository: v.optional(v.string()),
        }),
        type: v.union(
            v.literal("UPDATED"), 
            v.literal("CREATED")
        ),
        version: v.string()
    })
});